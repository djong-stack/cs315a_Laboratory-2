from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=1)
    publication_year: Optional[int] = None
    stock_quantity: int = Field(default=1, ge=0)
    category_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = Field(None, min_length=1)
    publication_year: Optional[int] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True