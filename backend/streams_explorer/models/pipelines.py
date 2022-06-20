from typing import List

from pydantic import BaseModel


class Pipelines(BaseModel):
    pipelines: List[str]
