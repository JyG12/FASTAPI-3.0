#pydantic models
from pydantic import BaseModel

class Book(BaseModel): #can name it as like CreateBook or wtv uw
    id: int
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