"""
Этот модуль описывает схему базы данных бота
-association_table описывает таблицу, которая реализует связь многие ко многим
между меню (pricing) и содежимым заказа
-User описывает таблицу пользователей приложения
-Order описывает таблицу с заказами
-Pricing описывает таблицу хранящую текущее меню
"""

from __future__ import annotations
from typing import List
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Time, ForeignKey, Table


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column('left_id', ForeignKey('orders.order_id'), primary_key=True),
    Column('right_id', ForeignKey('pricing.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(30), nullable=False)
    group = Column(String(4), nullable=False)
    phone_number = Column(String(15), nullable=False)

    orders: Mapped[List["Order"]] = relationship()


class Pricing(Base):
    __tablename__ = 'pricing'
    id = Column(Integer, primary_key=True)
    dish = Column(String(30))
    price = Column(Integer, nullable=False)

    orders: Mapped[List[Order]] = relationship(secondary=association_table, back_populates='pricing')


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer = Column(ForeignKey('users.id'))
    create_date = Column(DateTime, nullable=False)
    price = Column(Integer)
    delivery_time = Column(Time, nullable=False)
    status = Column(String(10), nullable=False)

    pricing: Mapped[List[Pricing]] = relationship(secondary=association_table, back_populates='orders')
