from fastapi import FastAPI

from src.api.crypto import router as crypto_router
from src.api.health import router as health_router
from src.core.middleware import value_error_handler
from src.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.middleware("http")(value_error_handler)

app.include_router(health_router)
app.include_router(crypto_router)
