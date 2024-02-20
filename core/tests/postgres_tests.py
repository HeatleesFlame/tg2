import random

import pytest

from core.postgres.query import postgres

user_list = [6318961470, 539190747]


@pytest.fixture()
def existing_user():
    return random.choice(user_list)


@pytest.fixture()
def non_existing_user():
    return random.randint(34543534, 67688687)


@pytest.fixture()
def user(non_existing_user):
    return {
        'tg_id': non_existing_user,
        'fullname': 'Test Testing',
        'group': 'test',
        'phone': 'phonenumber'
    }


@pytest.mark.asyncio
async def test_user_check_exists(existing_user):
    res = await postgres.check_user(existing_user)
    assert res is True


@pytest.mark.asyncio
async def test_user_check_non_exists(non_existing_user):
    res = await postgres.check_user(non_existing_user)
    assert res is False


@pytest.mark.asyncio
async def test_add_user(user):
    res = await postgres.add_user(user)
    assert res is None
