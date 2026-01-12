#all our models will be located in here
from sqlmodel import SQLModel, Field, Column, Relationship
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable = False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str 
    last_name: str
    role: str = Field(sa_column=Column(
        pg.VARCHAR, nullable = False, server_default="user"
    ))
    is_verified: bool = Field(default=False) #automatically sets it as False, means not verified
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    
"""
class User:
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = false
    created_at: datetime
    updated_at: datetime
"""

def __repr__(self):
    return f"<User {self.username}>"




class Book(SQLModel, table=True):
    __tablename__="books"

    uid: uuid.UUID = Field(
        sa_column=Column( #full control over database column
            pg.UUID,
            nullable = False, #cannot be empty
            primary_key = True, #unique identifier
            default = uuid.uuid4
        )
    ) #unique id

    title: str
    author: str
    publisher: str
    published_date: datetime #change to date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default = None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy":"selectin"})
    

    def __repr__(self):
        return f"<Book {self.title}>"
    


#create review
class Review(SQLModel, table=True):
    __tablename__="reviews"

    uid: uuid.UUID = Field(
        sa_column=Column( #full control over database column
            pg.UUID,
            nullable = False, #cannot be empty
            primary_key = True, #unique identifier
            default = uuid.uuid4
        )
    ) #unique id

    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default = None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default = None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default = datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
    


