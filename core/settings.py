r"""
Этот модуль содержит классы настроек бота:
-Bots содержит токен и айди администратора
-Databases содержит логин и пароль к базе данных
-Settings объединяет эти основные классы для удобного доступа
к настройкам из основного потока
-settings создает экземпляр класса Settings, с которым работает основная программа
"""

from environs import Env
from dataclasses import dataclass
import os


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    chef_id: int


@dataclass
class Databases:
    db_passwd: str
    db_login: str


@dataclass
class Settings:
    bots: Bots
    databases: Databases


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            chef_id=env.int('CHEF_ID')
        ),
        databases=Databases(
            db_passwd=env.str('DB_PASSWD'),
            db_login=env.str('DB_LOGIN')
        )
    )


settings = get_settings(os.path.join(os.path.dirname(__file__), '.env'))
