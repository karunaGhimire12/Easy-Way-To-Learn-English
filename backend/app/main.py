#backend/app/main.py 

from fastapi import FastAPI
from app.database import engine ,Base

Base.metadata.create_all(bind=engine)
app=FastAPI(title="sajilo English API")

@app.get("/")
def home():
    return {
        "message":"Welcome to Sajilo English!"
    }

 