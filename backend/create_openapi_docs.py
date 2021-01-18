import json
import os

from fastapi import FastAPI

from main import app

if __name__ == "__main__":
    print("Creating docs/openapi.json")
    doc_dir = "./docs"
    os.makedirs(doc_dir, exist_ok=True)
    with open(f"{doc_dir}/openapi.json", "w") as f:
        json.dump(FastAPI.openapi(app), f)
