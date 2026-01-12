#pydantic models
from pydantic import BaseModel
from datetime import datetime,date
from typing import List
import uuid
from src.reviews.schemas import ReviewModel

class Book(BaseModel): #can name it as like CreateBook or wtv uw
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    update_at: datetime
    

class BookDetailModel(Book):
    reviews: List[ReviewModel]
    
    
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel): #can name wtv uw, like UpdateBook
    title: str
    author: str
    publisher: str
    page_count: int
    language: str