from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from core.keyboards.reply import reply_keyboard_start


async def command_start_handler(message: Message, bot: Bot) -> None:
    """handle the command start event and say hello to user"""
    content = Text(
        "Hello, ",
        Bold(message.from_user.first_name)
    )
    await message.answer(
        **content.as_kwargs(), reply_markup=reply_keyboard_start
    )


async def create_order(message: Message, bot: Bot) -> None:
    """Обрабатывает создание заказа и заносит данные в БД"""
    await message.answer('Create')
    pass


async def remove_order(message: Message, bot: Bot) -> None:
    """Обрабатывает отмену заказа до указанного времени и обновляет статус в БД"""
    await message.answer('Remove')
    pass


async def order_delivered(message: Message, bot: Bot) -> None:
    "Обновляет статус заказа и завершает его"
    pass


async def non_supported(message: Message, bot: Bot) -> None:
    """Обрабатывает все события не полученные другими хендлерами"""
    await message.answer('Function not supported')
