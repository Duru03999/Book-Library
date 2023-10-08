#import necessary dependencies
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

import sqlite3

#import data handling libraries
from numpy import genfromtxt
#Import logging for error handling
import logging

#import local packages
from .model import Base, Book

#import base packages
import datetime
from time import time


#establish a connection with the database
# engine = create_engine('postgresql://username:password@localhost:5432/dbname')
engine = create_engine('sqlite:///books.db')

#define the path to the data file

file_name = './data/books.csv'

#create a session to interact with the database

Session = sessionmaker(bind=engine)
session = Session()

#function to load data from CSV file

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',',skip_header=1,dtype=None,invalid_raise=False,comments='|',encoding=None)
    print("rows: ",data.size)
    return data.tolist()

#function to initialize the database

async def InitDB():
    if not inspect(engine).has_table(Book.__tablename__):
        Base.metadata.create_all(engine)
        data = Load_Data(file_name)

        # with Session(engine) as session:
        try:
            for i in data:
                try:
                    book = Book(**{
                        'bookID': i[0],
                        'title': i[1],
                        'authors': i[2],
                        'average_Rating': i[3],
                        'ISBN': i[4],
                        'ISBN13': i[5],
                        'language_Code': i[6],
                        'num_Pages': i[7],
                        'ratings_Count': i[8],
                        'text_Reviews_Count': i[9],
                        'publication_Date': datetime.datetime.strptime(i[10],'%m/%d/%Y').date(),
                        'publisher': i[11]
                    })
                    session.add(book)
                except:
                    logging.warning(i[0])
            session.commit()
        except Exception as error:
            logging.error("rolling back",error)
            session.rollback()
        finally:
            session.close() #finished
    else:
        logging.info("Database already setup")    

