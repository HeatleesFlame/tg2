from aiogram.fsm.state import StatesGroup, State


class FillMenu(StatesGroup):
    filling = State()


class SendMenuPhoto(StatesGroup):
    sending_photo = State()


class CreateOrder(StatesGroup):
    choosing_dishes = State()
    choosing_time = State()
    sending_order = State()
