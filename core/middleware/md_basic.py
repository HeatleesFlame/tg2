"""
-этот модуль содержить миддлвари, которые обрабатывают апдейты
и выполняют запросы к БД
-register_check получает айди пользователя и проверяет наличие записи о нем в БД
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram.types import Update
from core.postgres.query import postgres
from core.redis_bridge.redis_bridge import redis_storage


async def register_check(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
) -> Any:
    """
    функция обрабатывает каждый апдейп поступивший от сервера
    и проверяет регистрацию отправившего его пользователя

    """
    try:
        if event.message.text == '/registration':
            await redis_storage.set(f'{data["event_from_user"].id}_reg', value='1', ex=300)
            return await handler(event, data)
    except AttributeError:
        pass

    if await redis_storage.get(f'{data["event_from_user"].id}_reg'):
        return await handler(event, data)

    if not await redis_storage.get(str(data['event_from_user'].id)):
        if await postgres.check_user(data['event_from_user'].id):
            await redis_storage.set(str(data['event_from_user'].id),
                                    'login')  # may overload sheets api if service attacked probably it configure good CI|CD to fix this fast
            return await handler(event, data)
        else:
            await event.message.answer('Тебя нет в табличке, зарегистрируйся /registration')
    else:
        return await handler(event, data)
