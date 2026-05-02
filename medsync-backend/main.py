from fastapi import FastAPI
from app.database import engine, Base
from app.routes import scan
from app.models import medication 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(scan.router)

@app.get("/")
def read_root():
    return {"message": "MedSync Backend is running!"}