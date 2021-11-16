import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from loguru import logger
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from streams_explorer.api.routes import api

# from streams_explorer.application import get_application
from streams_explorer.core.config import API_PREFIX, APP_NAME, settings
from streams_explorer.default import setup_default

# app = get_application()
app = FastAPI(title=APP_NAME)

app.include_router(api.router, prefix=API_PREFIX)

app.mount(
    "/_next/static", StaticFiles(directory="_next/static", html=True), name="static"
)


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("index.html")


app.add_event_handler("startup", setup_default(app))


@app.on_event("startup")
@repeat_every(seconds=settings.graph.update_interval)
async def update():
    logger.info("Update graph")
    await app.state.streams_explorer.update()
    logger.info("Update graph completed")


def start():
    # Run the main for debugging.
    # You can also use uvicorn to start the backend with auto reload on code changes:  uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
