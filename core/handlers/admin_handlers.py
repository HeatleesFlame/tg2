from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text
from core.keyboards.admin_kb import reply_admin_start,fill_menu_kb
from core.settings import settings
from core.FSMs.admin_FSMs import FillMenu

async def admin_start(message: Message, bot: Bot) -> None:
    """Эта функция привествует администратора и отправялет клавиатуру команд управления"""
    content = Text("Здравствуйте, ", Bold(message.from_user.first_name))
    await message.answer(**content.as_kwargs(), reply_markup=reply_admin_start)


async def fill_menu(message: Message, bot: Bot, state:FSMContext):
    if message.from_user.id == settings.bots.chef_id:
        content = Text("Введите название блюда и его цену вот так:\n'Название блюда' цена\nНазвание блюда указывается в одинарных кавычках, цена через пробел числом\nВ одном сообщении - одно блюдо\nКогда закончите нажмите кнопку \"Отправить меню\"")
        await message.answer(**content.as_kwargs(), reply_markup=fill_menu_kb)
        await state.set_state(FillMenu.filling)
