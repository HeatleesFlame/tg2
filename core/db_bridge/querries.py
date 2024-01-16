from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.db_bridge.models import User, Pricing, Order
from core.settings import settings

engine = create_async_engine(
    f'postgresql+asyncpg://{settings.databases.db_login}:{settings.databases.db_passwd}@localhost/tg_bot_db?prepared_statement_cache_size=500'
    # Создание машины соединений
)
async_session = async_sessionmaker(engine, expire_on_commit=False,
                                   autoflush=True)  # Создание фабрики сессий, для взаимодействия с БД


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


async def add_dish(dish, price) -> None:
    dish = Pricing(dish_name=dish, price=int(price))
    # TODO реализовать правильное заполнение меню, с обнулением счетчика айди
    async with async_session.begin() as session:
        session.add(dish)


async def truncate(table_name) -> None:
    """This function delete content and restart counter of id"""
    async with async_session.begin() as session:
        await session.delete(
            table_name)  # sqlalchemy.orm.exc.UnmappedInstanceError: Class 'sqlalchemy.orm.decl_api.DeclarativeAttributeIntercept' is not mapped; was a class (core.db_bridge.models.Pricing) supplied where an instanc


async def get_dishes() -> Iterable:
    async with async_session() as session:
        stmt = select(Pricing)
        result = await session.execute(stmt)
        return result.scalars().all()


async def commit_order(order: Order) -> None:
    async with async_session.begin() as session:
        session.add(order)


async def get_one_dish(identy: int) -> Pricing:
    async with async_session() as session:
        stmt = select(Pricing).where(Pricing.id == identy)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
