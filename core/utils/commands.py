from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='cancel',
            description='Отмена действия'
        ),
        BotCommand(
            command="registration",
            description='Регистрация'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
