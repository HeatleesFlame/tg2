from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def delete_button(keyboard: ReplyKeyboardMarkup, already_pressed: str) -> ReplyKeyboardMarkup:
    new_markup = keyboard
    already_pressed = already_pressed.split(' ')
    for text in already_pressed:
        try:
            new_markup.keyboard[0].remove(KeyboardButton(text=text))
        except ValueError:
            pass
    return new_markup
