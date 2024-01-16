"""
Этот модуль содержит клавиатуры бота
-reply_keyboard_start Описывает клавиатуру отправленную хендлером команды старт
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.db_bridge.querries import get_dishes

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

choose_time_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='13:35'),
        KeyboardButton(text='11:50'),
    ]
])

send_order_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить заказ')
    ]
])


async def build_menu() -> ReplyKeyboardMarkup:
    menu = await get_dishes()
    menu_kb = ReplyKeyboardBuilder()
    end_btn = KeyboardButton(text='Выбрать время')
    menu_kb.add(end_btn)
    for dish in menu:
        button = KeyboardButton(text=f'{dish.id}. {dish.dish_name}')
        menu_kb.add(button)
    return menu_kb.as_markup()


async def delete_button(keyboard: ReplyKeyboardMarkup, identy: int) -> ReplyKeyboardMarkup:
    buttons = []
    for btn in keyboard.keyboard[0]:
        buttons.append(btn)
    del buttons[identy + 1]
    return ReplyKeyboardMarkup(keyboard=[buttons])
