import psycopg2
from psycopg2.extras import RealDictCursor
import time

from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-addres/hostname>/<database_name>'

# Store the password in a variable so that there is no error due to the @ in the password
password = quote_plus(f'{settings.database_password}')



# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{password}@localhost/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, 
autoflush=False, bind=engine)

Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgrehiezen@9593548',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error", error)
#         time.sleep(2)
