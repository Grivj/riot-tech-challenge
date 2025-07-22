from fastapi import FastAPI

from src.api import crypto, health
from src.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.include_router(health.router)
app.include_router(crypto.router)
