import logging
import re
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from core.FSMs.FSM import CreateOrder, Form
from core.keyboards.admin_kb import ADMIN_START
from core.keyboards.user_kb import USER_START, DELIVERY_TIME, SEND_ORDER, MENU, DRINKS, \
    LUNCH, ASK_WISHES, USER_HOME
from core.keyboards.utils import delete_button
from core.postgres.query import postgres
from core.redis_bridge.redis_bridge import redis_storage
from core.settings import settings
from core.sheets_bridge.sheets_query import google_sheets


async def command_start_handler(message: Message, bot: Bot) -> None:
    """handle the command start event and say hello to user"""
    content = Text(
        "Привет, ",
        Bold(message.from_user.first_name)
    )
    if message.from_user.id == settings.bots.chef_id:
        await message.answer(**content.as_kwargs(), reply_markup=ADMIN_START)
    else:
        await message.answer(**content.as_kwargs(), reply_markup=USER_START)


async def command_registration(message: Message, bot: Bot, state: FSMContext) -> None:
    """Начинает процесс регистрации в боте"""
    if not await postgres.check_user(message.from_user.id):
        await message.answer('Укажите фамилию и имя, вот так:\nИванов Иван', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.name)
        user_info = {
            "tg_id": message.from_user.id,
            "fullname": '',
            'group': '',
            'phone': ''
        }
        await state.update_data(user_info=user_info)
    else:
        await message.answer('Вы уже зарегистрированы, спасибо!')


async def get_name(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Добавляет """
    if re.fullmatch(pattern=r'[А-Я][а-я]+ [А-Я][а-я]+', string=message.text):
        await message.answer('Будем знакомы! Теперь укажите свой класс:\nНапример, 9В')
        user_data = await state.get_data()
        user_data['user_info']['fullname'] = message.text
        await state.update_data(user_data)
        await state.set_state(Form.group)
    else:
        await message.answer('Не очень-то это и похоже на твое имя и фамилию(')


async def get_group(message: Message, bot: Bot, state: FSMContext) -> None:
    if re.fullmatch(pattern=r'\d+[А-Я]', string=message.text):
        await message.answer('Отлично, теперь укажи номер телефона\nНапример, вот так: +71234566789')
        user_data = await state.get_data()
        user_data['user_info']['group'] = message.text
        await state.update_data(user_data)
        await state.set_state(Form.phone)
    else:
        await message.answer('Что-то не так, попробуй еще раз')


async def get_phone_end_reg(message: Message, bot: Bot, state: FSMContext) -> None:
    if re.fullmatch(pattern=r'\+\d{11}', string=message.text):
        if message.from_user.id == settings.bots.chef_id:
            await message.answer('Вы успешно зарегистировались!', reply_markup=ADMIN_START)
        else:
            await message.answer(f'Вот и все, теперь можешь делать заказы!', reply_markup=USER_START)
        user_data = await state.get_data()
        await state.clear()
        user_data['user_info']['phone'] = message.text
        await state.update_data(user_data)
        await postgres.add_user(user_data['user_info'])
        return await google_sheets.add_user(user=user_data['user_info'])
    else:
        await message.answer('Не похоже на номер, попробуй еще раз')


async def create_order(message: Message, bot: Bot, state: FSMContext) -> None:
    if await redis_storage.get(f'{message.from_user.id}_order'):
        await message.answer('У вас уже есть активный заказ, вы сможете сделать новый когда отправят меню',
                             reply_markup=USER_HOME)
    else:
        await state.set_state(CreateOrder.choosing_dishes)
        await message.answer('Нажмите на обед, который хотите заказать', reply_markup=LUNCH)
        await message.answer('Также вы можете собрать обед самостоятельно', reply_markup=MENU)
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
    await callback.message.answer('Записал. Выберите напиток, если его нет в клавиатуре, просто напишите',
                                  reply_markup=DRINKS)
    await state.set_state(CreateOrder.choosing_beverage)


async def get_dish(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.text in ["Суп", "Салат", "Второе"]:

        user_data = await state.get_data()
        user_data['order']['content'] += f'{message.text} '
        await state.update_data(data=user_data)

        new_kb = delete_button(keyboard=MENU,
                               already_pressed=user_data['order']['content'])
        await message.answer('Записал',
                             reply_markup=new_kb)
    else:
        await message.answer(f'Я вас не совсем понимаю, вы правда хотели заказать {message.text}?)')


async def ask_drink(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.answer('Выберите напиток, если его нет в клавиатуре, просто напишите', reply_markup=DRINKS)
    await state.set_state(CreateOrder.choosing_beverage)


async def get_drink(message: Message, bot: Bot, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['order']['content'] += f'{message.text} '
    await state.update_data(user_data)

    await state.set_state(CreateOrder.choosing_time)
    await message.answer('Записал, когда хотите получить заказ?', reply_markup=DELIVERY_TIME)


async def get_time(message: Message, bot: Bot, state: FSMContext) -> None:
    if re.fullmatch(r'\d\d:\d\d', message.text):
        user_data = await state.get_data()
        user_data['order']['delivery_time'] += message.text
        await state.update_data(user_data)
        await state.set_state(CreateOrder.write_wishes)
        await message.answer('Записал, есть какие-нибудь пожелания к заказу', reply_markup=ASK_WISHES)
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
    await message.answer(reply_text, reply_markup=SEND_ORDER)


async def send_order(message: Message, bot: Bot, state: FSMContext) -> None:
    user_data = await state.get_data()
    await state.clear()

    content = user_data['order']['content']
    delivery_time = user_data['order']['delivery_time']
    wishes = user_data['order']['wishes']

    await message.answer(f'Заказ отправлен:\n{content}\nВремя выдачи:\n{delivery_time}\nПожелания к заказу:\n{wishes}',
                         reply_markup=USER_HOME)

    await redis_storage.set(f'{message.from_user.id}_order', '1')

    return await google_sheets.commit_order(user_data['order'])


async def remove_order(message: Message, bot: Bot, state: FSMContext) -> None:
    user_id = message.from_user.id
    await state.set_data({})
    await redis_storage.delete(f'{user_id}_order')
    await bot.send_message(chat_id=settings.bots.chef_id,
                           text=f'Заказ номер {user_id} был отменен')  # search is inconvenient for users
    await message.answer('Ваш заказ был отменен, мы уже сообщили об этом', reply_markup=USER_START)
    pass


async def cancel(message: Message, bot: Bot, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Нечего отменять')
        return
    if current_state in Form.__states__:
        await message.answer('Закончи регистрацию!')
        return
    else:
        logging.info('Action has cancelled ')
        await state.clear()
        if message.from_user.id != settings.bots.chef_id:
            await message.answer('Действие отменено', reply_markup=USER_START)
        else:
            await message.answer('Действие отмено', reply_markup=ADMIN_START)


async def non_supported(message: Message, bot: Bot) -> None:
    """Обрабатывает все события, не полученные другими хендлерами"""
    await message.answer('Не совсем понимаю о чем вы(')
