import asyncpg
from fastapi import APIRouter, Depends
import app.core.database as db
from app.core.security import verify_firebase_token

router = APIRouter()

@router.get("/api/classes")
async def get_classes(conn: asyncpg.Connection = Depends(db.get_connection), token = Depends):
    print(token)

@router.get("/api/classes/{class_id}")
async def get_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    query = "SELECT schedule, section, subject_name, subject_code, class_id FROM classes WHERE class_id = $1"
    class_data = await conn.fetchrow(query, class_id)

    if not class_data:
        return {"message": "Class not Found"}

    return {"content":dict(class_data)}

