from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user

app = FastAPI(title="Marketplace API")

@app.get("/")
def root():
    return {"message": "Marketplace API running"}

