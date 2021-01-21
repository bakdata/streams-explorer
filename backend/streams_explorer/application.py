from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from streams_explorer.api.routes import api
from streams_explorer.core.config import API_PREFIX, APP_NAME


def get_application() -> FastAPI:
    application = FastAPI(title=APP_NAME)
    application.mount(
        "/static", StaticFiles(directory="static", html=True), name="static"
    )

    @application.get("/")
    @application.get("/static")
    def frontend():
        return RedirectResponse(url="/static/")

    application.include_router(api.router, prefix=API_PREFIX)
    return application
