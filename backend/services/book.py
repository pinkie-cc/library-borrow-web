from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_


from models.categories import Category
from models.book import Book
from schemas.book import BookCreate, BookUpdate
from schemas.response_custom import ResponseSchema


def create_book(book: BookCreate, db: Session) -> ResponseSchema:
    try:
        new_book = Book(**book.model_dump())
        new_book.available_quantity = new_book.quantity
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e._message())}",
        )

    return ResponseSchema(
        status="success",
        message="Book created successfully",
        data=new_book,
    )

# Put /book/{book_id}: Update book details (admin only) check if the book exists, and if exists, check the available quantity and compare it with the new quantity and update the details.
def update_book(book_id: int, book: BookUpdate, db: Session) -> ResponseSchema:
    try:
        book_db = db.query(Book).filter(Book.id == book_id).first()
        if not book_db:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            ) 
        # model_dump: converts a pydantic model instance into a plain python dictionary.
        update_data = book.model_dump(exclude_unset=True)

        if "quantity" in update_data:
            new_quantity = update_data["quantity"]
            borrowed_count = book_db.quantity - book_db.available_quantity

            # ตรวจสอบว่า new_quantity ไม่ต่ำกว่าจำนวนที่ถูกยืมอยู่
            if new_quantity < borrowed_count:
                raise HTTPException(
                    status_code=404,
                    detail=f"Cannot set quantity lower than borrowed count ({borrowed_count})",
                )

            update_data["available_quantity"] = new_quantity - borrowed_count

        # set book_db.key=value
        for key, value in update_data.items():
            setattr(book_db, key, value)

        db.commit()
        db.refresh(book_db)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e._message())}",
        )

    return ResponseSchema(
        status="success",
        message="Book updated successfully",
        data=book_db,
    )


def get_all_books(db: Session) -> ResponseSchema:
    try:
        books_db = db.query(Book).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e._message())}",
        )

    return ResponseSchema(
        status="success",
        message="Books fetched successfully",
        data=books_db,
    )


def get_books_by_query(
    db: Session, category_name: Optional[str] = None, book_name: Optional[str] = None
) -> ResponseSchema:
    try:
        query = db.query(Book).join(Category)
        if book_name:
            # search for books by title(case insensitive)
            query = query.filter(Book.title.ilike(f"%{book_name}%"))
        if category_name:
            query = query.filter(Category.name.ilike(f"%{category_name}%"))
        books_db = query.all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e._message())}",
        )

    return ResponseSchema(
        status="success",
        message="Books fetched successfully",
        data=books_db,
    )
