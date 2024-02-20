import pytest
from core.sheets_bridge.core_scripts import list_users, clear_order_table


@pytest.mark.asyncio
async def test_list_users():
    res = await list_users()
    assert type(res) is list


@pytest.mark.asyncio
async def test_clear_order_table():
    res = await clear_order_table()
    assert res is None
