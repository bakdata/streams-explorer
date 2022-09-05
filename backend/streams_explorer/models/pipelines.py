from pydantic import BaseModel


class Pipelines(BaseModel):
    pipelines: list[str]
