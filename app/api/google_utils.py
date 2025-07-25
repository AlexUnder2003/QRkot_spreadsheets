from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.constants import REPORT_TIME_FORMAT, SPREADSHEET_BODY


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(REPORT_TIME_FORMAT)
    service = await wrapper_service.discover("sheets", "v4")
    spreadsheet_body_template = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body = spreadsheet_body_template
    spreadsheet_body["properties"]["title"] = spreadsheet_body["properties"][
        "title"
    ].format(now_date_time=now_date_time)
    response = await wrapper_service.as_user(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"], response["spreadsheetUrl"]


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
