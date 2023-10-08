from fastapi import Request, Response, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse

import datetime

from data.service import session, InitDB
from data.model import Book
from data.repositories import BookRepository

import logging

app = FastAPI()

# default for the root to go to the auto-generated document page
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')

# GET all the books
@app.get("/books")
async def books():
    return BookRepository.get_all()

# GET the count of books in the database
@app.get("/books/count")
async def bookCount():
    return BookRepository.count()

# POST a new book to the database
@app.post("/books",status_code=status.HTTP_201_CREATED)
async def book(request: Request):
    newBookJson = await request.json()          
    newBook = Book(**newBookJson)
    newBook.publication_Date = datetime.datetime.strptime(newBook.publication_Date,'%Y-%m-%d').date()
    # save
    try:
        BookRepository.save(newBook)
        return newBook #return
    except Exception as error:
        raise HTTPException(status_code=500,detail="error creating")

# PUT an update to a book to the database
@app.put("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def book(request: Request, id: int):
    updateBookJson = await request.json()          
    updateBook = Book(**updateBookJson)
    if updateBook.publication_Date:
        updateBook.publication_Date = datetime.datetime.strptime(updateBook.publication_Date,'%Y-%m-%d').date()
    
    # save
    try:
        BookRepository.update(updateBook,id)
    except Exception as error:
        raise HTTPException(status_code=500,detail="error updating")

# DELETE a book
@app.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def book(id: int):
    try:
        BookRepository.delete(id)
    except Exception as error:
        raise HTTPException(status_code=500,detail="error updating")


# GET search by title, author, publisher, or year
@app.get("/books/search")
async def bookSearch(title: str | None = None, publisher: str | None = None, author: str | None = None,year: str | None = None):
    if title:        
        return BookRepository.get_by_title(title)
    if publisher:
        return BookRepository.get_by_publisher(publisher)
    if author:
        return BookRepository.get_by_author(author)
    if year:
        return BookRepository.get_by_year(year)        
    return "[]" # default return


# GET book by specific id
@app.get("/books/{id}")
async def bookById(id: int):
    return BookRepository.get_by_id(id)



# startup event to initiate database
@app.on_event("startup")
async def app_startup():
    await InitDB()