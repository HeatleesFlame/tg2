import json
import os.path
from datetime import datetime
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from core.settings import settings


class GoogleSheets:
    def __init__(self, spreadsheet_id: str):

        if os.path.exists('test_service_account.json'):
            self.service_account_key = json.load(
                open(r'test_service_account.json'))
        else:
            self.service_account_key = json.load(
                open(r'../../test_service_account.json'))

        self.background_tasks = set()

        self.sheets = None
        self.creds = ServiceAccountCreds(
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
            **self.service_account_key
        )

        self.aiogoogle = Aiogoogle(service_account_creds=self.creds)

        self.spreadsheet_id = spreadsheet_id

        self.tg = None

    async def _create_api(self, name='sheets', version='v4') -> None:
        """API instance creating"""
        async with self.aiogoogle as aiogoogle:
            self.sheets = await aiogoogle.discover(name, version)

    async def add_user(self, user: dict) -> None:
        if not self.sheets:
            await self._create_api()

        user = [[val for val in user.values()]]

        async with self.aiogoogle as aiogoogle:
            await aiogoogle.as_service_account(
                self.sheets.spreadsheets.values.append(
                    spreadsheetId=self.spreadsheet_id,
                    range='users!A2:D',
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    json={
                        "majorDimension": 'ROWS',
                        "values": user
                    }
                ))

    async def commit_order(self, order: dict) -> None:
        if not self.sheets:
            await self._create_api()
        order = [[values for values in order.values()]]
        #  create delivery date
        t = datetime.now(settings.timezone)
        if t.hour > 16:
            order[0].append(f'=DATE({t.year}, {t.month}, {t.day + 1})')
        else:
            order[0].append(f'=DATE({t.year}, {t.month}, {t.day})')
        # format time for sheets
        order[0][2] = '=TIME({0};{1};00)'.format(*order[0][2].split(':'))

        async with self.aiogoogle as aiogoogle:  # noqa
            response = await aiogoogle.as_service_account(self.sheets.spreadsheets.values.append(
                spreadsheetId=self.spreadsheet_id,
                range='orders!A2:E',
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                json={
                    "majorDimension": 'ROWS',
                    "values": order
                }

            ))

    async def clear_order_table(self) -> None:
        if not self.sheets:
            await self._create_api()
        async with self.aiogoogle as aiogoogle:
            response = await aiogoogle.as_service_account(
                self.sheets.spreadsheets.values.get(
                    spreadsheetId=self.spreadsheet_id,
                    range="orders!A2:E",
                    majorDimension="ROWS")
            )

            if 'values' in response.keys():
                values = response['values']
            else:
                return
            res = await aiogoogle.as_service_account(
                self.sheets.spreadsheets.values.append(
                    spreadsheetId=self.spreadsheet_id,
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
                self.sheets.spreadsheets.values.clear(spreadsheetId=self.spreadsheet_id, range="orders!A2:E"))


google_sheets = GoogleSheets(spreadsheet_id='1I8nNZUOBK7HGLDWsRwHwUbEtT6E4rlXsbITHbvgNuv4')
