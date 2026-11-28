#backend/app/main.py 

from fastapi import FastAPI
from .database import engine ,Base
from  .import models
from  app.auth.router import router as auth_router
from app.vocabulary.router import router as vocabulary_router

Base.metadata.create_all(bind=engine)
app=FastAPI(title="sajilo English API")

@app.get("/")
def home():
    return {
        "message":"Welcome to Sajilo English!"
    }

app.include_router(auth_router)
app.include_router(vocabulary_router)
 