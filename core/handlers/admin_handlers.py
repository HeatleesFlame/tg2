from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import InputMediaPhoto
from core.postgres.query import postgres
from core.keyboards.admin_kb import SEND_MENU, ADMIN_START
from core.keyboards.user_kb import USER_START
from core.redis_bridge.redis_bridge import del_from_pattern
from core.sheets_bridge.sheets_query import google_sheets
from core.FSMs.FSM import SendMenuPhoto
from core.settings import settings


async def get_link_to_spreadsheet(message: Message, bot: Bot) -> None:
    """
    Отправляет администратору ссылку на таблицы
    Или сообщает о том, что у пользователя нет доступа
    """
    if message.from_user.id == settings.bots.chef_id:
        link = f'https://docs.google.com/spreadsheets/d/{settings.google_api.spreadsheet_id}'
        await message.answer(link)
    else:
        await message.answer('Вы не являетесь администратором')


async def wait_menu_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    """
    Меняет состояние администратора
    и создает хранилище для фото
    """
    if message.from_user.id == settings.bots.chef_id:
        await state.set_state(SendMenuPhoto.sending_photos)
        await state.set_data({'photos': []})
        await message.answer('Отправьте фото меню, когда закончите, еще раз нажмите отправить.\nОтправляйте фото по одному!',
                             reply_markup=SEND_MENU)
    else:
        await message.answer('Вы не являетесь администратором')


async def get_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    """Добавляет ссылку на фото в хранилище"""
    if not message.photo:
        await message.answer('Это не фото')
        return
    user_data = await state.get_data()
    user_data['photos'].append(message.photo[-1].file_id)
    await state.update_data(photos=user_data['photos'])
    await message.answer('Скачал')


async def send_photos(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправляет фото, отпраленные администратором всем авторизованным пользователям"""
    if message.from_user.id == settings.bots.chef_id:
        user_data = await state.get_data()

        if not user_data['photos']:
            await message.answer('Вы не отправили ни одного фото')
            return

        await message.answer('Фото будут отправлены пользователям', reply_markup=ADMIN_START)
        await state.clear()
        media_group = []
        # сборка медиагруппы для отправки
        for photo in user_data['photos']:
            media_group.append(InputMediaPhoto(media=photo))

        await del_from_pattern('*_order')
        # реализация рассылки меню
        async for user in postgres.list_users():
            if user != settings.bots.chef_id:
                await bot.send_media_group(chat_id=user, media=media_group)
                await bot.send_message(text='Теперь можно сделать заказ', reply_markup=USER_START, chat_id=user)
        # перенос данных из таблицы заказов для дня в таблицу для всех заказов
        return await google_sheets.clear_order_table()
