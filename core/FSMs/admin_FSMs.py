from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


class FillMenu(StatesGroup):
    filling = State()


class SendMenuPhoto(StatesGroup):
    sending_photo = State()
