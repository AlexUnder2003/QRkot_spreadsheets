CHARITY_PROJECT_NAME_MIN_LENGTH = 3
CHARITY_PROJECT_NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 1

USER_PASSWORD_LEN = 3

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
REPORT_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = {
    "properties": {
        "title": "Отчет на {now_date_time}",
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
