import asyncpg
from fastapi import APIRouter, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
import app.db.repositories.grade_repository as grade_repository
from app.db.models.grade_model import AssessmentModel


router = APIRouter()

@router.get("/api/classes/{class_id}/grade_types")
async def get_grade_types():
    pass


@router.post("/api/classes/{class_id}/{type_name}/assessments")
async def insert_assessment(class_id: int, type_name:str, conn: asyncpg.Connection = Depends(db.get_connection)):
    res = await grade_repository.insert_assessment_to_db(conn, class_id, type_name)
