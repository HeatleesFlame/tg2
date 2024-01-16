from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from memory_profiler import profile
from core.FSMs.FSM import CreateOrder
from core.db_bridge.models import Order
from core.db_bridge.querries import commit_order, get_one_dish
from core.keyboards.admin_kb import reply_admin_start
from core.keyboards.user_kb import reply_keyboard_start, build_menu, delete_button, choose_time_kb, send_order_kb
from core.settings import settings


async def command_start_handler(message: Message, bot: Bot) -> None:
    """handle the command start event and say hello to user"""
    content = Text(
        "Hello, ",
        Bold(message.from_user.first_name)
    )
    if message.from_user.id == settings.bots.chef_id:
        await message.answer(**content.as_kwargs(), reply_markup=reply_admin_start)
    else:
        await message.answer(**content.as_kwargs(), reply_markup=reply_keyboard_start)


async def create_order(message: Message, bot: Bot, state: FSMContext) -> None:
    keyboard = await build_menu()
    await message.answer('Нажмите на блюдо, которое хотели бы заказать\nКогда закончите, напишите Отправить заказ',
                         reply_markup=keyboard)
    order = Order(customer=message.from_user.id, status='Создан')
    await state.set_state(CreateOrder.choosing_dishes)
    await state.update_data(order=order, keyboard=keyboard)


async def get_order_entity(message: Message, bot: Bot, state: FSMContext) -> None:
    # TODO реализовать обработку некорректного ввода
    # TODO реализовать удаление выбранных позиций меню из клавиатуры
    dish_id, dish_name = message.text.split('.')  # получаем айди товара и название
    dish_id = int(dish_id)

    # if dish_name in [dish.dish_name for dish in await get_dishes()]:  # may cause performance issues
    user_data = await state.get_data()  # получаем данные из фсм

    dish = await get_one_dish(dish_id)  # загружаем товар из бд
    user_data['order'].pricing.append(dish)  # добавляем к заказу

    new_keyboard = await delete_button(user_data['keyboard'], identy=dish_id)  # удаляем кнопку с товаром
    await message.answer('Принял', reply_markup=new_keyboard)

    await state.update_data()
    # else:
    #   await message.answer('Вы указали блюдо неверно\nЕсли ошибки нет, обратитесь к администратору')


async def ask_time(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.set_state(CreateOrder.choosing_time)
    await message.answer('Выберите время', reply_markup=choose_time_kb)


async def get_time(message: Message, bot: Bot, state: FSMContext):
    user_data = await state.get_data()
    order = user_data['order']
    order.delivery_time = message.text
    await state.update_data(order=order)
    await state.set_state(CreateOrder.sending_order)
    await message.answer('Записал', reply_markup=send_order_kb)


async def send_order(message: Message, bot: Bot, state: FSMContext) -> None:  # TODO оптимизировать процесс создания заказа и реализовать расчет его стоимости с учетом скидки если попадает под опредленный шаблон
    user_data = await state.get_data()
    await commit_order(user_data['order'])
    await message.answer("Заказ отправлен")
    await state.clear()


async def remove_order(message: Message, bot: Bot) -> None:
    """Обрабатывает отмену заказа до указанного времени и обновляет статус в БД"""
    await bot.send_message(chat_id=settings.bots.chef_id,
                           text='Заказ номер ХХХ был отменен')  # TODO реализовать удаление записи о заказе из базы данных а также наложить ограничения на отмену
    await message.answer('Ваш заказ был отменен, мы уже сообщили об этом')
    pass


async def order_delivered(message: Message, bot: Bot) -> None:
    "Обновляет статус заказа и завершает его"
    pass


async def non_supported(message: Message, bot: Bot) -> None:
    """Обрабатывает все события, не полученные другими хендлерами"""
    await message.answer('Function not supported')
