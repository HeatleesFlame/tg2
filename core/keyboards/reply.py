"""
Этот модуль содержит клавиатуры бота
-reply_keyboard_start Описывает клавиатуру отправленную хендлером команды старт
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_keyboard_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сделать заказ'
        ),
        KeyboardButton(
            text='Отменить заказ'
        ),
        KeyboardButton(text='Заказ получен')
    ]],
    resize_keyboard=True,
    input_field_placeholder='Выбери кнопку'
)
