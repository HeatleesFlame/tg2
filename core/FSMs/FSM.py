from aiogram.fsm.state import StatesGroup, State


class SendMenuPhoto(StatesGroup):
    """Этот класс описывает состояние отправки фотографий меню"""
    sending_photos = State()


class CreateOrder(StatesGroup):
    """Этот класс описывает состояния при создании заказа"""
    choosing_dishes = State()
    choosing_time = State()
    choosing_beverage = State()
    sending_order = State()
    write_wishes = State()


class Form(StatesGroup):
    """Этот класс описывает состояния при заполнении данных о себе"""
    name = State()
    group = State()
    phone = State()
