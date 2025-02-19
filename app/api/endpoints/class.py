import asyncpg
from fastapi import APIRouter, Depends
import app.core.database as db

router = APIRouter()

@router.get("/api/classes")
async def get_classes(conn: asyncpg.Connection = Depends(db.get_connection), token = Depends):
    print(token)

@router.get("api/classes/{class_id}")
async def get_class(conn: asyncpg.Connection = Depends(db.get_connection()):
    pass
