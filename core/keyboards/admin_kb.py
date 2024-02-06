from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_admin_start = ReplyKeyboardMarkup(keyboard=[
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

