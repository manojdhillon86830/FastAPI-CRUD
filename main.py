from fastapi import FastAPI
from crud.api import router
from database import Base, engine


# Create tables in the database if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the API router
app.include_router(router)


