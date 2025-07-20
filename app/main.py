from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.core.init import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
