"""
Этот модуль содержит клавиатуры бота
-reply_keyboard_start Описывает клавиатуру отправленную хендлером команды старт
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сделать заказ'
        ),
    ]],
    resize_keyboard=True,
    input_field_placeholder='Выбери кнопку'
)

user_home = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отменить заказ'
        ),
    ]],
    resize_keyboard=True,
    input_field_placeholder='Выбери кнопку'
)

choose_time_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='13:35'),
        KeyboardButton(text='11:50'),
    ],
], one_time_keyboard=True
)

send_order_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить заказ')
    ]
])

menu_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Суп'),
        KeyboardButton(text='Второе'),
        KeyboardButton(text="Салат"),
    ],
    [
        KeyboardButton(text='Выбрать напиток'),
    ]
],
    resize_keyboard=True
)

beverage_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Чай'),
        KeyboardButton(text='Морс'),
        KeyboardButton(text='Вода'),
    ],
],
    resize_keyboard=True
)

wishes_kb = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Нет, спасибо!')
]], resize_keyboard=True
)

complex_dinner = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Комплексный обед 1',
            callback_data='complex_1'
        )],
    [InlineKeyboardButton(
        text='Комплексный обед 2',
        callback_data='complex_2'
    )],
    [
        InlineKeyboardButton(
            text='Комплексный обед 3',
            callback_data='complex_3'
        )]

]
)


async def delete_button(keyboard: ReplyKeyboardMarkup, already_pressed: str) -> ReplyKeyboardMarkup:
    already_pressed = already_pressed.split(' ')
    for text in already_pressed:
        try:
            keyboard.keyboard[0].remove(KeyboardButton(text=text))
        except ValueError:
            pass
    return keyboard
