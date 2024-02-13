from aiogram.fsm.state import StatesGroup, State


class FillMenu(StatesGroup):
    filling = State()


class SendMenuPhoto(StatesGroup):
    sending_photos = State()


class CreateOrder(StatesGroup):
    choosing_dishes = State()
    choosing_time = State()
    choosing_beverage = State()
    sending_order = State()
    write_wishes = State()


class Form(StatesGroup):
    name = State()
    group = State()
    phone = State()
