import asyncpg
from fastapi import APIRouter, Depends
import app.core.database as db
from app.core.security import verify_firebase_token
from app.db.models.class_model import ClassModel
import app.db.repositories.class_repository as class_repository

router = APIRouter()

@router.get("/api/classes")
async def get_classes(conn: asyncpg.Connection = Depends(db.get_connection), token = Depends(verify_firebase_token)):
    res = await class_repository.get_classes_from_db(conn)
    return {"classes": res}


@router.post("/api/classes")
async def get_class(class_body: ClassModel, conn: asyncpg.Connection = Depends(db.get_connection)):
    res = await class_repository.insert_class_into_db(conn, class_body)
    return {"class_id": res}

@router.delete("/api/classes/{class_id}")
async def delete_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    # Get the class data
    class_data = await class_repository.get_class_from_db(conn, class_id)

    # Delete the class row from db
    await class_repository.delete_class_from_db(conn, class_id)

    return {"class": class_data}