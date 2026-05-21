from fastapi import FastAPI
from app.config import settings
from app.endpoints import items

print(settings.DATABASE_URL_psycopg)

app = FastAPI(title="Lab 2", version="1.0")

app.include_router(items.router)
