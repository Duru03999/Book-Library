#import dependencies
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import datetime
from time import time

class Base(DeclarativeBase):
    pass
    
class Book(Base):
    __tablename__ = "Book"
    bookID: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    authors: Mapped[str]
    average_Rating: Mapped[float]
    ISBN: Mapped[str]
    ISBN13: Mapped[str]
    language_Code: Mapped[str]
    num_Pages: Mapped[int]
    ratings_Count: Mapped[str]
    text_Reviews_Count: Mapped[int]
    publication_Date: Mapped[datetime.datetime]
    publisher: Mapped[str]