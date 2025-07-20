from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.constants import REPORT_TIME_FORMAT


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(REPORT_TIME_FORMAT)
    service = await wrapper_service.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {
            "title": f"Отчет на {now_date_time}",
            "locale": "ru_RU",
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": 4, "columnCount": 100},
                }
            }
        ],
    }
    response = await wrapper_service.as_user(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def spreadsheets_update_value(
    spreadsheetid: str,
    data: list,
    wrapper_service: Aiogoogle,
) -> None:
    now_date_time = datetime.now().strftime(REPORT_TIME_FORMAT)
    service = await wrapper_service.discover("sheets", "v4")
    table_values = [
        ["Отчет от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for project, days_diff in data:
        new_row = [
            project.name,
            str(days_diff),
            project.description,
        ]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_service.as_user(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:C30",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
