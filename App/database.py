from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from App.config import settings

# URL encode the password to handle special characters
encoded_password = quote(settings.database_password, safe="")
SQL_Alchemy_Database_URL = f"postgresql+psycopg://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQL_Alchemy_Database_URL)
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()

