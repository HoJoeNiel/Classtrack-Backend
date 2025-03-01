import asyncpg
from fastapi import APIRouter, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
from app.api.endpoints.auth_endpoint import verify_user
from app.db.models.class_model import ClassModel
import app.db.repositories.class_repository as class_repository
from app.db.models.class_model import Students, Content

router = APIRouter()

@router.get("/api/classes")
async def get_classes(conn: asyncpg.Connection = Depends(db.get_connection), user: dict = Depends(verify_user)):
    prof_id = user["uid"]
    res = await class_repository.get_classes_from_db(conn, prof_id)
    return {"classes": res}


@router.post("/api/classes")
async def insert_class(class_body: ClassModel, conn: asyncpg.Connection = Depends(db.get_connection), user: dict = Depends(verify_user)):
    prof_id = user["uid"]
    res = await class_repository.insert_class_into_db(conn, class_body, prof_id)
    return {"class_id": res}

@router.delete("/api/classes/{class_id}")
async def delete_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    # Get the class data
    class_data = await class_repository.get_class_from_db(conn, class_id)

    # Delete the class row from db
    await class_repository.delete_class_from_db(conn, class_id)

    return {"class": class_data}

@router.get("/api/classes/{class_id}")
async def get_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    # query = "SELECT class_size, schedule, section, subject_name, subject_code, class_id FROM classes WHERE class_id = $1"
    # class_data = await conn.fetchrow(query, class_id)

    class_data = await class_repository.get_class_from_db(conn, class_id)

    return {"content": class_data}

@router.get("/api/classes/{class_id}/students", response_model=Content)
async def get_students_from_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    # query = "SELECT * FROM students WHERE class_id = $1"
    # students = await conn.fetch(query, class_id)

    students = await class_repository.get_students_from_classes_table(conn, class_id)


    if not students:
        raise HTTPException(status_code=404, detail="Class not found.")
    
    students_list = [Students(**dict(student))for student in students]
    return {"content": students_list}


@router.post("/api/students")
async def insert_student(studentModel: Students, conn: asyncpg.Connection = Depends(db.get_connection)):

    await class_repository.insert_student_to_db(studentModel, conn)

    return {'message': 'Student successfully added.'}

# Delete attendance record using class_id and student_number
@router.delete("/api/classes/{classId}/students/{student_number}")
async def delete_student_from_class(class_id: int, student_number: str, conn: asyncpg.Connection = Depends(db.get_connection)):
    result = await class_repository.delete_student_to_db(conn, class_id, student_number)
    return result == "DELETE 1"  # Returns True if a record was deleted

    