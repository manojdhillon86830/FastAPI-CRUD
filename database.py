from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Direct database connection 
# SQLALCHEMY_DATABASE_URL = "postgresql://myuser:Dhillon@86830@localhost/manoj"
SQLALCHEMY_DATABASE_URL = "postgresql://manoj:manoj@localhost/manoj"




# Creating the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# SessionLocal for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
