from typing import List

from pydantic.main import BaseModel


class Pipelines(BaseModel):
    pipelines: List[str]
