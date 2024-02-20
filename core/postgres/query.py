import asyncio
from typing import Iterable, Iterator

import asyncpg

from core.settings import settings
connection_str = f'postgresql://{settings.postgres.postgres_user}:{settings.postgres.postgres_passwd}@localhost/{settings.postgres.db_name}'


class PostgresQuery:
    def __init__(self, connection_string):
        self._pool: asyncpg.Pool = None  # noqa
        self.connection_string = connection_string

    async def create_pool(self) -> None:
        self._pool = await asyncpg.create_pool(dsn=self.connection_string)

    async def add_user(self, user_info: dict):
        """
        insert user info to tables
        user_info must contain these keys:
        tg_id: contain user's telegram id
        fullname: contain user's fullname
        group: contain user's group
        phone: contain user's phone number
        """
        if not self._pool:
            await self.create_pool()
        async with self._pool.acquire() as conn:
            await conn.execute("""
                    INSERT INTO users
                    VALUES ($1, $2, $3, $4)
                    """, *user_info.values())

    async def check_user(self, tg_id: int) -> bool:
        if not self._pool:
            await self.create_pool()
        async with self._pool.acquire() as conn:
            user = await conn.fetchval("SELECT tg_id FROM users where tg_id = $1 ", tg_id)
            if user:
                return True
            else:
                return False

    async def list_users(self) -> Iterator[int]:
        if not self._pool:
            await self.create_pool()
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                async for user in conn.cursor('SELECT tg_id FROM users'):
                    yield user.get('tg_id')


postgres = PostgresQuery(connection_string=connection_str)

