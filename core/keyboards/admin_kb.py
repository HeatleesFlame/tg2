from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ADMIN_START = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить фото меню'
            ),
        KeyboardButton(
            text='Получить ссылку на таблицы'
        )
    ]], resize_keyboard=True,
        one_time_keyboard=True
)
SEND_MENU = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Отправить')
]])
