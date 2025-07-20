from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.google_utils import spreadsheets_create, spreadsheets_update_value
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud

router = APIRouter(prefix="/google", tags=["google"])


@router.get("/")
async def google_import_to_sheets(
    wrapper_service: Aiogoogle = Depends(get_service),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех закрытых благотворительных проектов
    по скорости заполнения.

       Формирует отчет в Google Sheets.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheet_id = await spreadsheets_create(wrapper_service)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_service)
    spreadsheet_url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    )
    return spreadsheet_url
