import asyncpg
from fastapi import APIRouter, Body, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
import app.db.repositories.grade_repository as grade_repository
from app.db.models.grade_model import AssessmentModel, ScoreList
from typing import Annotated

router = APIRouter()

@router.get("/api/classes/{class_id}/grade_types")
async def get_grade_types():
    pass


@router.post("/api/classes/{class_id}/{type_name}/assessments")
async def insert_assessment(assessment_model: Annotated[AssessmentModel, Body(embed=True)],
                            class_id: int,
                            type_name:str, 
                            conn: asyncpg.Connection = Depends(db.get_connection)):
    await grade_repository.insert_assessment_to_db(conn, class_id, type_name, assessment_model)

    return {'message': 'Assessment Successfully Created'}

@router.delete("/api/classes/{class_id}/{grade_type_id}/assessments/{assessment_id}")
async def delete_assessment(class_id: int, grade_type_id: int, assessment_id:int, conn: asyncpg.Connection = Depends(db.get_connection)):
    
    await grade_repository.delete_assessment_to_db(class_id, grade_type_id, assessment_id, conn)

    return {'message': f"assessment successfully deleted."}

@router.get("/api/classes/{class_id}/{grade_type_id}/scores")
async def get_scores(class_id: int, grade_type_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):

    res = await grade_repository.get_scores_from_db(class_id, grade_type_id, conn)
    # print(res)
    return {'content': res}


@router.put("/api/classes/{class_id}/scores")
async def update_scores(class_id: int, model:ScoreList, conn: asyncpg.Connection = Depends(db.get_connection)):
    res = await grade_repository.update_scores_to_db(class_id, model, conn)
    return {'message': res}