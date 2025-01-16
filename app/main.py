from fastapi import FastAPI
from app.routes import rates

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Unified API!"}

app.include_router(rates.router, prefix="/api/v1")