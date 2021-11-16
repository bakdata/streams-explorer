from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from streams_explorer.api.routes import api
from streams_explorer.core.config import API_PREFIX, APP_NAME


def get_application() -> FastAPI:
    app = FastAPI(title=APP_NAME)
    app.include_router(api.router, prefix=API_PREFIX)

    app.mount("/", StaticFiles(directory="static", html=True), name="static")

    return app
