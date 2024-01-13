"""
-этот модуль содержить миддлвари, которые обрабатывают апдейты
и выполняют запросы к БД
-register_check получает айди пользователя и проверяет наличие записи о нем в БД
"""


from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, Update
from core.db_bridge.querries import check


async def register_check(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    """
    функция обрабатывает каждый апдейп поступивший от сервера
    и проверяет регистрацию отправившего его пользователя

    """

    if await check(identy=data['event_from_user'].id):  # we check if user is registered
        return await handler(event, data)
    else:
        await event.message.answer('you are not registered')  # if user isn't registered we drop update
        return
