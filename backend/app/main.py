from fastapi import FastAPI
app=FastAPI(title="sajilo English API")

@app.get("/")
def home():
    return {
        "message":"Welcome to Sajilo English!"
    }