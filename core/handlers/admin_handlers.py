from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.user_kb import reply_keyboard_start
from core.redis_bridge.redis_bridge import del_from_pattern
from core.sheets_bridge.core_scripts import list_users, clear_order_table
from core.FSMs.FSM import SendMenuPhoto
from core.settings import settings


async def get_link_to_spreadsheet(message: Message, bot: Bot) -> None:
    if message.from_user.id == settings.bots.chef_id:
        link = f'https://docs.google.com/spreadsheets/d/{settings.google_api.spreadsheet_id}'
        await message.answer(link)
    else:
        await message.answer('А тебе зачем?')


async def wait_menu_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.from_user.id == settings.bots.chef_id:
        await state.set_state(SendMenuPhoto.sending_photo)
        await message.answer('Отправьте фото меню, учтите, что таблица заказов будет очищена')
    else:
        await message.answer('Ты вроде не админ(')


async def get_menu_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.answer('Фото будет отправлено пользователям')
    await clear_data()
    photo = message.photo[-1]
    for user in await list_users():
        if user != f'{settings.bots.chef_id}':
            await bot.send_photo(chat_id=user, photo=photo.file_id,reply_markup=reply_keyboard_start)
        else:
            pass
    await state.clear()


async def clear_data() -> None:
    await del_from_pattern('*_order')
    await clear_order_table()
