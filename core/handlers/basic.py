import logging
import re

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold

from core.FSMs.FSM import CreateOrder
from core.keyboards.admin_kb import reply_admin_start
from core.keyboards.user_kb import reply_keyboard_start, choose_time_kb, send_order_kb, menu_kb, beverage_kb, \
    complex_dinner, wishes_kb, user_home, delete_button
from core.redis_bridge.redis_bridge import redis_storage
from core.settings import settings
from core.sheets_bridge.core_scripts import commit_order


async def command_start_handler(message: Message, bot: Bot) -> None:
    """handle the command start event and say hello to user"""
    content = Text(
        "Привет, ",
        Bold(message.from_user.first_name)
    )
    if message.from_user.id == settings.bots.chef_id:
        await message.answer(**content.as_kwargs(), reply_markup=reply_admin_start)
    else:
        await message.answer(**content.as_kwargs(), reply_markup=reply_keyboard_start)


async def create_order(message: Message, bot: Bot, state: FSMContext) -> None:
    if await redis_storage.get(f'{message.from_user.id}_order'):
        await message.answer('У вас уже есть активный заказ, вы сможете сделать новый когда отправят меню', reply_markup=user_home)
    else:
        await state.set_state(CreateOrder.choosing_dishes)
        await message.answer('Нажмите на обед, который хотите заказать', reply_markup=complex_dinner)
        await message.answer('Также вы можете собрать обед самостоятельно', reply_markup=menu_kb)
        await state.set_data(
            {
                'order': {
                    'customer': str(message.from_user.id),
                    'content': '',
                    'delivery_time': '',
                    'wishes': ''
                }
            }
        )


async def complete_dinner(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    order = user_data['order']

    match callback.data:
        case 'complex_1':
            order['content'] += 'Суп Второе Салат Хлеб '
        case 'complex_2':
            order['content'] += 'Суп Второе Хлеб '
        case 'complex_3':
            order['content'] += 'Второе Салат Хлеб '

    await state.update_data(order=order)
    await callback.message.answer('Записал. Выберите напиток, если его нет в клавиатуре, просто напишите', reply_markup=beverage_kb)
    await state.set_state(CreateOrder.choosing_beverage)


async def get_dish(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.text in ["Суп", "Салат", "Второе"]:
        user_data = await state.get_data()
        user_data['order']['content'] += f'{message.text} '
        await state.update_data(data=user_data)
        new_kb = await delete_button(keyboard=menu_kb, already_pressed=user_data['order']['content'])
        await message.answer('Записал', reply_markup=new_kb)
    else:
        await message.answer(f'Я вас не совсем понимаю, вы правда хотели заказать {message.text}?)')


async def ask_drink(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.answer('Выберите напиток, если его нет в клавиатуре, просто напишите', reply_markup=beverage_kb)
    await state.set_state(CreateOrder.choosing_beverage)


async def get_drink(message: Message, bot: Bot, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['order']['content'] += f'{message.text} '
    await state.update_data(user_data)
    await state.set_state(CreateOrder.choosing_time)
    await message.answer('Записал, когда хотите получить заказ?', reply_markup=choose_time_kb)


async def get_time(message: Message, bot: Bot, state: FSMContext) -> None:
    if re.fullmatch(string=message.text, pattern='\d\d:\d\d'):  # noqa
        user_data = await state.get_data()
        user_data['order']['delivery_time'] += message.text
        await state.update_data(user_data)
        await state.set_state(CreateOrder.write_wishes)
        await message.answer('Записал, есть какие-нибудь пожелания к заказу', reply_markup=wishes_kb)
    else:
        await message.answer('Не время, друх, не время...')


async def get_wishes(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.text != 'Нет, спасибо!':
        reply_text = 'Мы уже учли ваши пожелания!'
        user_data = await state.get_data()
        user_data['order']['wishes'] += message.text
        await state.update_data(user_data)
    else:
        reply_text = 'Пора отправлять заказ, или отменить - (/cancel)'
    await state.set_state(CreateOrder.sending_order)
    await message.answer(reply_text, reply_markup=send_order_kb)


async def send_order(message: Message, bot: Bot, state: FSMContext) -> None:
    user_data = await state.get_data()
    content = user_data['order']['content']
    delivery_time = user_data['order']['delivery_time']
    wishes = user_data['order']['wishes']
    await message.answer(f'Заказ отправлен:\n{content}\nВремя выдачи:\n{delivery_time}\nПожелания к заказу:\n{wishes}', reply_markup=user_home)
    user_data = user_data['order']
    await redis_storage.set(f'{message.from_user.id}_order', '1')
    # build order representation as sheets values
    values = [[]]
    for key in user_data.keys():
        values[0].append(user_data[key])
    await commit_order(order=values)
    await state.clear()


async def remove_order(message: Message, bot: Bot, state: FSMContext) -> None:
    user_id = message.from_user.id
    await state.set_data({})
    await redis_storage.delete(f'{user_id}_order')
    await bot.send_message(chat_id=settings.bots.chef_id,
                           text=f'Заказ номер {user_id} был отменен')  # search is inconvenient for users
    await message.answer('Ваш заказ был отменен, мы уже сообщили об этом', reply_markup=reply_keyboard_start)
    pass


# async def order_delivered(message: Message, bot: Bot) -> None:
#     """Обновляет статус заказа и завершает его"""
#     # function not used in current version but kept for pay from credit card
#     pass


async def cancel(message: Message, bot: Bot, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Нечего отменять')
        return
    else:
        logging.info('Action has cancelled ')
        await state.clear()
        if message.from_user.id != settings.bots.chef_id:
            await message.answer('Действие отменено', reply_markup=reply_keyboard_start)
        else:
            await message.answer('Действие отмено', reply_markup=reply_admin_start)


async def non_supported(message: Message, bot: Bot) -> None:
    """Обрабатывает все события, не полученные другими хендлерами"""
    await message.answer('Не совсем понимаю о чем вы(')
