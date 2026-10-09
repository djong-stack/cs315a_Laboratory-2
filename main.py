from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Book Inventory API",
    description="RESTful Web API for managing books and categories (CS 315a Midterm)",
    version="1.0.0",
)


@app.post(
    "/categories/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Categories"],
)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    return crud.create_category(db=db, category=category)


@app.get(
    "/categories/", response_model=List[schemas.CategoryResponse], tags=["Categories"]
)
def read_categories(db: Session = Depends(get_db)):
    """Retrieve a list of all categories."""
    return crud.get_categories(db=db)


@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Add a new book (must belong to an existing category)."""
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.BookResponse], tags=["Books"])
def read_books(
    category_id: Optional[int] = Query(
        None, description="Optional filter by category_id"
    ),
    db: Session = Depends(get_db),
):
    """Retrieve all books. Supports optional filtering: /books/?category_id=1"""
    return crud.get_books(db=db, category_id=category_id)


@app.get("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve details of a specific book by ID."""
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def update_book(
    book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)
):
    """Update book information (partial update)."""
    return crud.update_book(db=db, book_id=book_id, book_update=book_update)


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Remove a book from inventory."""
    return crud.delete_book(db=db, book_id=book_id)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Library Book Inventory API is running", "docs": "/docs"}
