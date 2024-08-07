from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject
from app.service import AppSpreadsheet


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(AppSpreadsheet.FORMAT)
    service = await wrapper_services.discover("sheets",
                                              AppSpreadsheet.SHEETS_API_VERSION
                                              )
    spreadsheet_body = {
        "properties": {
            "title": f"{AppSpreadsheet.TITLE} {now_date_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": AppSpreadsheet.TITLE,
                    "gridProperties": {
                        "rowCount": AppSpreadsheet.RAW_COUNT,
                        "columnCount": AppSpreadsheet.COLUMN_COUNT,
                    },
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive",
                                              AppSpreadsheet.SHEETS_API_VERSION
                                              )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list[CharityProject],
    wrapper_services: Aiogoogle,
):
    """Сохраняет информацию в гугл таблицу"""
    now_date_time = datetime.now().strftime(AppSpreadsheet.FORMAT)
    service = await wrapper_services.discover("sheets",
                                              AppSpreadsheet.SHEETS_API_VERSION
                                              )
    table_values = [
        ["Отчёт от", now_date_time],
        ["Топ проектов по скорости закрытия."],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for charity_project in charity_projects:
        new_row = [
            str(charity_project.name),
            str(charity_project.close_date - charity_project.create_date),
            str(charity_project.description),
        ]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=AppSpreadsheet.RANGE,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
