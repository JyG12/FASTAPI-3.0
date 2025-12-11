#book activity
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Shadow Hunters",
        "author": "Cassandra Clare",
        "publisher": "Margaret K. McElderry Books",
        "published_date": "2007-03-27",
        "page_count": 485,
        "language": "English"
    },
    {
        "id": 2,
        "title": "I Want to Die but I Want to Eat Tteokbokki",
        "author": "Baek Sehee",
        "publisher": "Bloomsbury Publishing",
        "published_date": "2018-06-20",
        "page_count": 192,
        "language": "English"
    },
    {
        "id": 3,
        "title": "Marigold Laundry",
        "author": "Local Singapore Author",
        "publisher": "Marigold Press",
        "published_date": "2021-02-14",
        "page_count": 250,
        "language": "English"
    },
    {
        "id": 4,
        "title": "The Cat Book: POV of a Cat",
        "author": "Whiskers McFluff",
        "publisher": "Feline House Publishing",
        "published_date": "2020-10-10",
        "page_count": 160,
        "language": "English"
    },
    {
        "id": 5,
        "title": "Bookstore",
        "author": "Literary Lane",
        "publisher": "Book Haven Press",
        "published_date": "2019-07-01",
        "page_count": 210,
        "language": "English"
    },
    {
        "id": 6,
        "title": "Shadow Hunters: The Sequel",
        "author": "Cassandra Clare",
        "publisher": "Margaret K. McElderry Books",
        "published_date": "2009-08-04",
        "page_count": 550,
        "language": "English"
    }
]

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

@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book)-> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail = "Book not found")

@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data:BookUpdateModel) -> dict:
    
    for book in books:
        if book['id'
                ] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {} #theres nth to return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



