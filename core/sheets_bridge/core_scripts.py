import json
import logging
from typing import List
from memory_profiler import profile
from aiogoogle import Aiogoogle, GoogleAPI
from aiogoogle.auth.creds import ServiceAccountCreds
from core.settings import settings

service_account_key = json.load(
    open(r'test_service_account.json'))  # no abs path in production fix this

creds = ServiceAccountCreds(
    scopes=[
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/devstorage.full_control",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ],
    **service_account_key
)

spreadsheet_id = settings.google_api.spreadsheet_id


async def create_api(name: str, version: str) -> GoogleAPI:
    """API instance creating"""
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:  # noqa
        return await aiogoogle.discover(name, version)


@profile
async def is_user(
        user_id: int) -> bool or None:  # this function may cause performance issues because pulls all users data to ram
    sheets = await create_api(name='sheets', version='v4')
    async with Aiogoogle(service_account_creds=creds) as aiogoogle: # noqa
        user = await aiogoogle.as_service_account(
            sheets.spreadsheets.values.get(
                spreadsheetId=spreadsheet_id,
                range='users!A2:A',
                majorDimension='COLUMNS'
            )
        )
        for identy in user['values'][0]:
            if int(identy) == user_id:
                return True
        return False


async def list_users():
    sheets = await create_api(name='sheets', version='v4')
    async with Aiogoogle(service_account_creds=creds) as aiogoogle: # noqa
        users_list = await aiogoogle.as_service_account(sheets.spreadsheets.values.get(
            spreadsheetId=spreadsheet_id,
            range='users!A2:A',
            majorDimension='COLUMNS'
        )
        )
        return users_list['values'][0]


# sheet = asyncio.run(get_user(539190747)) # testing
# print(sheet)
# user_list = asyncio.run(list_users()) # testing
# print(user_list)


async def commit_order(order: List[List[str]]) -> None:
    sheets = await create_api(name='sheets', version='v4')
    order[0].append('=TODAY()')
    async with Aiogoogle(service_account_creds=creds) as aiogoogle: # noqa
        response = await aiogoogle.as_service_account(sheets.spreadsheets.values.append(
            spreadsheetId=spreadsheet_id,
            range='orders!A2:E',
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            json={
                "majorDimension": 'ROWS',
                "values": order
            }

        ))
    if response:
        logging.info(msg='order successfully commited to tables')


# res = asyncio.run(commit_order([["3445454", "somecontent", "sometime", "somewish"]]))  #
# print(res)  # tests


async def clear_order_table() -> None:
    sheets = await create_api(name='sheets', version='v4')
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        values = await aiogoogle.as_service_account(
            sheets.spreadsheets.values.get(
                spreadsheetId=spreadsheet_id,
                range="orders!A2:E",
                majorDimension="ROWS")
        )
        values = values['values']
        await aiogoogle.as_service_account(
            sheets.spreadsheets.values.append(
                spreadsheetId=spreadsheet_id,
                range="allorders!A2:E",
                json={
                    "majorDimension": "ROWS",
                    "values": values
                },
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
            )
        )
        await aiogoogle.as_service_account(
            sheets.spreadsheets.values.clear(spreadsheetId=spreadsheet_id, range="orders!A2:E"))
