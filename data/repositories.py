from typing import Iterator
from sqlalchemy import func
from sqlalchemy.orm import Session
import datetime

from .model import Book
from .service import session

import logging

class BookRepository:

    # Get all books from the database

    def get_all() -> Iterator[Book]:
        return session.query(Book).all()

    # Get the count of books in the database
    
    def count():
        return session.query(func.count(Book.bookID)).scalar()

    #Get a book by its ID
    
    def get_by_id(id: int):
        return session.query(Book).filter(Book.bookID == id).all()

    #Search for books by title
    def get_by_title(title: str): 
        return session.query(Book).filter(Book.title.like('%' + title + '%')).all()

    # Search for books by publisher
    
    def get_by_publisher(publisher: str):
        return session.query(Book).filter(Book.publisher.like('%' + publisher + '%')).all()

    # Search for books by author
    
    def get_by_author(author: str):
        return session.query(Book).filter(Book.authors.like('%' + author + '%')).all()

    # Search for books published in a specific year
    
    def get_by_year(year: str):
        return session.query(Book).filter(Book.publication_Date >= year + '-01-01').filter(Book.publication_Date <= year + '-12-31').all()

    # Save a new book to the database
    
    def save(book: Book):
        try:
            session.add(book)
            session.commit()
            session.refresh(book)
            return book
        except Exception as error:
            logging.error("Exception occurred",error)
            session.rollback()
            raise

        # Update an existing book in the database
        

    def update(updateBook: Book,id: int):
            # retrieve the book by id
            # set values
            # save
            try:
                existingBook = BookRepository.get_by_id(id)[0]            
                # loop
                for a in dir(updateBook):                
                    if not a.startswith('_') and not callable(getattr(updateBook, a)) and a != 'registry' and a != 'metadata':
                        updateVal = getattr(updateBook,a)
                        if updateVal:
                            setattr(existingBook,a,updateVal)
                # flush changes
                session.commit()
                session.flush()
            except Exception as error:
                logging.error("Exception occurred",error)
                session.rollback()
                raise

    def delete(id: int):
        try:
            existingBook = BookRepository.get_by_id(id)[0]
            session.delete(existingBook)
            session.commit()
            session.flush()
        except Exception as error:
            logging.error("Exception occurred",error)
            session.rollback()
            raise