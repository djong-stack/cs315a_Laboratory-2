from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional
import models
import schemas


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    category = get_category(db, book.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {book.category_id} does not exist",
        )

    db_book = models.Book(
        title=book.title,
        isbn=book.isbn,
        publication_year=book.publication_year,
        stock_quantity=book.stock_quantity,
        category_id=book.category_id,
    )
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ISBN already exists (must be unique)",
        )


def get_books(db: Session, category_id: Optional[int] = None):
    query = db.query(models.Book)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    return query.all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )

    update_data = book_update.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = get_category(db, update_data["category_id"])
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {update_data['category_id']} does not exist",
            )

    for field, value in update_data.items():
        setattr(db_book, field, value)

    try:
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ISBN already exists (must be unique)",
        )


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    db.delete(db_book)
    db.commit()
    return {"detail": f"Book with id {book_id} has been deleted"}
