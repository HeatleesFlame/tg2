import asyncio
import logging

from aiogram import Dispatcher, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import any_state
from aiogram.fsm.storage.redis import RedisStorage
from memory_profiler import profile

from core.FSMs.FSM import SendMenuPhoto, CreateOrder
from core.handlers.admin_handlers import wait_menu_photo, get_menu_photo, get_link_to_spreadsheet
from core.handlers.basic import command_start_handler, create_order, remove_order, non_supported, \
    get_dish, send_order, get_time, ask_drink, get_drink, cancel, complete_dinner, get_wishes
from core.middleware.md_basic import register_check
from core.redis_bridge.redis_bridge import redis_storage
from core.settings import settings
from core.utils.commands import set_commands


async def start_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bots started!')


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bot stopped!')


@profile
async def start():
    logging.basicConfig(level=logging.INFO,
                        filename='logs.log',
                        filemode='w'
                        )
    storage = RedisStorage(redis=redis_storage)
    bot = Bot(settings.bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    await set_commands(bot)

    dp.update.outer_middleware(register_check)  # for testing check is disabled
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    dp.message.register(command_start_handler, Command(commands=['start']))
    dp.message.register(cancel, Command(commands=['cancel']), any_state)
    # admin handler registry
    dp.message.register(get_link_to_spreadsheet, F.text == 'Получить ссылку на таблицы')
    dp.message.register(wait_menu_photo, F.text == 'Отправить фото меню')
    dp.message.register(get_menu_photo, SendMenuPhoto.sending_photo)

    # user handler registry

    dp.message.register(create_order, F.text == 'Сделать заказ')
    dp.callback_query.register(complete_dinner, F.data.startswith('complex'))
    dp.message.register(ask_drink, F.text == 'Выбрать напиток', CreateOrder.choosing_dishes)
    dp.message.register(get_dish, CreateOrder.choosing_dishes)
    dp.message.register(get_drink, CreateOrder.choosing_beverage)
    dp.message.register(get_time, CreateOrder.choosing_time)
    dp.message.register(get_wishes, CreateOrder.write_wishes)
    dp.message.register(send_order, F.text == 'Отправить заказ', CreateOrder.sending_order)
    dp.message.register(remove_order, F.text == 'Отменить заказ')
    dp.message.register(non_supported)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
