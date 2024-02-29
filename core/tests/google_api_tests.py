import random

import pytest

from core.sheets_bridge.sheets_query import google_sheets


@pytest.fixture()
def user():
    return {
        "tg_id": random.randint(34535, 676867876),
        "fullname": 'Test Testing',
        'group': 'test',
        'phone': 'test_phone'
    }


@pytest.fixture()
def order():
    return {
        'customer': random.randint(34545, 4455665),
        'content': 'Test content',
        'delivery time': '11:50',
        'wishes': 'None'
    }


@pytest.mark.asyncio
async def test_add_user(user):
    res = await google_sheets.add_user(user)
    assert None is None


@pytest.mark.asyncio
async def test_commit_order(order):
    res = await google_sheets.commit_order(order)
    assert None is None
