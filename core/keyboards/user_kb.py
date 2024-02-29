"""
Этот модуль содержит клавиатуры бота
-reply_keyboard_start Описывает клавиатуру отправленную хендлером команды старт
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

USER_START = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сделать заказ'
        ),
    ]],
    resize_keyboard=True,
    input_field_placeholder='Выбери кнопку'
)

USER_HOME = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отменить заказ'
        ),
    ]],
    resize_keyboard=True,
    input_field_placeholder='Выбери кнопку'
)

DELIVERY_TIME = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='13:35'),
        KeyboardButton(text='11:50'),
    ],
], one_time_keyboard=True
)

SEND_ORDER = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить заказ')
    ]
])

MENU = ReplyKeyboardMarkup(keyboard=[
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

DRINKS = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Чай'),
        KeyboardButton(text='Морс'),
        KeyboardButton(text='Вода'),
    ],
],
    resize_keyboard=True
)

ASK_WISHES = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Нет, спасибо!')
]], resize_keyboard=True
)

LUNCH = InlineKeyboardMarkup(inline_keyboard=[
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
