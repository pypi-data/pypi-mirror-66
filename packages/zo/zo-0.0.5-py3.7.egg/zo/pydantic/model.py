from pydantic import BaseModel
from typing import Any


class BaseModelValidation(BaseModel):
    class Config:
        validate_assignment = True


class BaseModelWithoutValidation(BaseModel):  # same as BaseModel
    class Config:
        validate_assignment = False  # default


class BaseModelInitDemo(BaseModel):  # same as BaseModel
    demo: str = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.demo = '...'
