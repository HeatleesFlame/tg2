from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from core.db_bridge.models import User
from core.settings import settings

engine = create_async_engine(
    f'postgresql+asyncpg://{settings.databases.db_login}:{settings.databases.db_passwd}@localhost/tg_bot_db?prepared_statement_cache_size=500'  # Создание машины соединений
)
async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)  # Создание фабрики сессий, для взаимодействия с БД


async def check(identy) -> bool:  
    """
    Возвращает буль тру если есть пользователь с переданным айди
    и фолс если такой записи в БД нет
    :param identy: айди пользователя отправившего апдейт
    """
    async with async_session() as session:
        stmt = select(User.id).where(User.id == identy)
        result = await session.execute(stmt)
        return bool(result.first())


async def user_list() -> Iterable:
    async with async_session() as session:
        result = await session.execute(select(User.id))
        return result
