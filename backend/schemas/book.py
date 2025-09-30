from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated, Optional, List

from schemas.category import CategoryResponse



class BookBase(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1)]
    author: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    year: Optional[int] = Field(default=None, ge=1000, le=2100)
    quantity: Optional[int] = None
    available_quantity: Optional[int] = None


class BookCreate(BookBase):
    category_id: int

class BookUpdate(BookBase):
    category_id : int
    quantity: Optional[int] = None
    # pass


class BookResponse(BookBase):
    id: int
    category: CategoryResponse
  
    class Config:
        from_attributes = True
