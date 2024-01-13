from aiogram import Dispatcher, Bot, F, Router
from aiogram.enums import ParseMode
from core.db_bridge.querries import engine
from core.db_bridge.models import Base
from core.handlers.basic import command_start_handler, create_order, remove_order, order_delivered, non_supported
from core.handlers.admin_handlers import admin_start, fill_menu
from core.middleware.md_basic import register_check
import asyncio
from core.settings import settings
from aiogram.filters import Command
import logging
from core.utils.commands import set_commands


async def start_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bots started!')
    await set_commands(bot)


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bot stopped!')


async def start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logging.basicConfig(level=logging.INFO,
                        # format='%(asctime)s - [%levelname)s - %(name)s - '
                        #      '(%(filename)s.%(funcName)s(%lineno)d) - %(message)s', #ошибка форматирования лога
                        filename='logs.log',
                        filemode='w'
                        )
    bot = Bot(settings.bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.update.outer_middleware(register_check)
    dp.message.register(fill_menu, F.text == 'Заполнить меню')
    dp.message.register(admin_start, F.from_user.id == settings.bots.chef_id)
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
    dp.message.register(command_start_handler, Command(commands=['start']))
    dp.message.register(create_order, F.text == 'Сделать заказ')
    dp.message.register(remove_order, F.text == 'Отменить заказ')
    dp.message.register(order_delivered, F.text == 'Заказ получен')
    dp.message.register(non_supported)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
