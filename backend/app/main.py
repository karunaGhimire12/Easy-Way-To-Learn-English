#backend/app/main.py 

from fastapi import FastAPI
from .database import engine ,Base
from  .import models

Base.metadata.create_all(bind=engine)
app=FastAPI(title="sajilo English API")

@app.get("/")
def home():
    return {
        "message":"Welcome to Sajilo English!"
    }

 