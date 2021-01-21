from pydantic.main import BaseModel, List


class Pipelines(BaseModel):
    pipelines: List[str]
