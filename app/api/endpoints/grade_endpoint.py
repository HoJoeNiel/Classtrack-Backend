import asyncpg
from fastapi import APIRouter, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
import app.db.repositories.grade_repository as grade_repository
from app.db.models.grade_model import Students, Content


router = APIRouter()

@router.get("/api/classes/{class_id}/grade_types")
async def get_grade_types():
    pass