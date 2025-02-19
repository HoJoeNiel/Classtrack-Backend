import asyncpg
from fastapi import APIRouter, Depends
import app.core.database as db
from app.core.security import verify_firebase_token
from app.db.models.class_model import Students, Class, Content

router = APIRouter()

@router.get("/api/classes")
async def get_classes(conn: asyncpg.Connection = Depends(db.get_connection), token = Depends):
    print(token)

@router.get("/api/classes/{class_id}")
async def get_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    query = "SELECT class_size, schedule, section, subject_name, subject_code, class_id FROM classes WHERE class_id = $1"
    class_data = await conn.fetchrow(query, class_id)

    if not class_data:
        return {"message": "Class not Found"}

    return {"content":dict(class_data)}

@router.get("/api/classes/{class_id}/students", response_model=Content)
async def get_students_from_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    query = "SELECT * FROM students WHERE class_id = $1"
    students = await conn.fetch(query, class_id)

    if not students:
        return {"message": "Class not found"}
    
    students_list = [Students(**dict(student))for student in students]
    return {"content": students_list}