from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables
import models_a
import models_b
import routes_b
import routes_a

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Zadaća 2 - REST API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(routes_a.router)
app.include_router(routes_b.router)

@app.get("/")
def read_root():
    return {"message": "Zadaća 2 - REST API"}