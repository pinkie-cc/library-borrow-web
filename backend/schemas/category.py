from pydantic import BaseModel
from pydantic.types import StringConstraints
from typing import Annotated


class CategoryCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]

class CategoryResponse(BaseModel):
    id: int
    name: Annotated[str, StringConstraints(min_length=1)]