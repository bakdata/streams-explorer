from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from streams_explorer.api.routes import api
from streams_explorer.core.config import API_PREFIX, APP_NAME


def get_application() -> FastAPI:
    app = FastAPI(title=APP_NAME)
    app.mount(
        "/_next/static", StaticFiles(directory="_next/static", html=True), name="static"
    )

    @app.get("/", include_in_schema=False)
    async def index():
        return FileResponse("index.html")

    @app.get("/{path}", include_in_schema=False)
    async def public(path: str):
        return FileResponse(path)

    app.include_router(api.router, prefix=API_PREFIX)
    return app
