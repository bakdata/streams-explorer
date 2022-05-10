import uvicorn as uvicorn
from fastapi_utils.tasks import repeat_every
from loguru import logger

from streams_explorer.application import get_application
from streams_explorer.core.config import settings
from streams_explorer.default import setup_default

app = get_application()

app.add_event_handler("startup", setup_default(app))


@app.on_event("startup")
async def watch():
    await app.state.streams_explorer.watch()


@app.on_event("startup")
@repeat_every(seconds=settings.graph.update_interval)
async def update():
    logger.info("Update graph")
    await app.state.streams_explorer.update()
    logger.info("Update graph completed")


@app.on_event("startup")
@repeat_every(seconds=settings.kafkaconnect.update_interval)
async def update_connectors():
    if not settings.kafkaconnect.url:
        return
    app.state.streams_explorer.update_connectors()


def start():
    # Run the main for debugging.
    # You can also use uvicorn to start the backend with auto reload on code changes:  uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
