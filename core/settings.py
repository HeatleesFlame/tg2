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
    host: str
    port: int


@dataclass
class Postgres:
    postgres_passwd: str
    postgres_user: str
    postgres_db: str


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
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT')
        ),
        google_api=GoogleApi(
            spreadsheet_id=env.str('SPREADSHEET_ID')
        ),
        postgres=Postgres(
            postgres_user=env.str('POSTGRES_USER'),
            postgres_passwd=env.str('POSTGRES_PASSWORD'),
            postgres_db=env.str('POSTGRES_DB')
        )
    )


settings = get_settings(os.path.join(os.path.dirname(__file__), '.env'))
