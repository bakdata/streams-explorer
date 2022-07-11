from __future__ import annotations

from pydantic import BaseModel


class Pipelines(BaseModel):
    pipelines: list[str]
