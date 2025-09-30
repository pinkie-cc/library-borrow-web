from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from borrow import Borrows  

# Base tells that this is not just a python class, but a table in the database.
# __tablename__ specifies the name of the table in the database.
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="borrower")
# Establishes a one-to-many relationship with the Borrows model, allowing access to all borrow records associated with a user.
    borrows: Mapped[List["Borrows"]] = relationship("Borrows", back_populates="user")
