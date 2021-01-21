import uvicorn as uvicorn

from streams_explorer.application import get_application
from streams_explorer.default import setup_default

app = get_application()
app.add_event_handler("startup", setup_default(app))

if __name__ == "__main__":
    # Run the main for debugging.
    # You can also use uvicorn to start the backend with auto reload on code changes:  uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
