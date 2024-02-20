r"""
Этот модуль содержит классы настроек бота:
-Bots содержит токен и айди администратора
-Databases содержит логин и пароль к базе данных
-Settings объединяет эти основные классы для удобного доступа
к настройкам из основного потока
-settings создает экземпляр класса Settings, с которым работает основная программа
"""
from __future__ import annotations
from environs import Env
from dataclasses import dataclass
import os


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    chef_id: int


@dataclass
class Redis:
    user_name: str
    passwd: str
    addr: str


@dataclass
class Postgres:
    postgres_passwd: str
    postgres_user: str
    db_name: str


@dataclass
class GoogleApi:
    spreadsheet_id: str


@dataclass
class Settings:
    bots: Bots
    redis: Redis
    google_api: GoogleApi
    postgres: postgres


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            chef_id=env.int('CHEF_ID')
        ),
        redis=Redis(
            user_name=env.str('REDIS_USER'),  # configure redis client later
            passwd=env.str('REDIS_PASSWORD'),
            addr=env.str('REDIS_ADDR')
        ),
        google_api=GoogleApi(
            spreadsheet_id=env.str('SPREADSHEET_ID')
        ),
        postgres=Postgres(
            postgres_user=env.str('POSTGRES_USER'),
            postgres_passwd=env.str('POSTGRES_PASSWORD'),
            db_name=env.str('DB_NAME')
        )
    )


settings = get_settings(os.path.join(os.path.dirname(__file__), '.env'))
