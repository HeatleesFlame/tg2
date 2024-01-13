from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_admin_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить фото меню'
            ),
        KeyboardButton(
            text='Заполнить меню'
        ),
    ]], resize_keyboard=True,
)

fill_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить меню'
        )
    ]
])
