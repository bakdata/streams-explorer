import json
from pathlib import Path

from fastapi import FastAPI

from main import app

if __name__ == "__main__":
    print("Creating docs/openapi.json")
    doc_dir = Path.cwd() / "docs"
    doc_dir.mkdir(exist_ok=True)
    with open(doc_dir / "openapi.json", "w") as f:
        json.dump(FastAPI.openapi(app), f)
