from fastapi import APIRouter, Depends
import app.core.database as db
from app.core.security import verify_firebase_token
import app.db.repositories.grade_repository as grade_repository
from app.db.models.grade_model import GradeType


router = APIRouter()


@router.get("/api/classes/{class_id}/grade_types")
async def get_grade_types(class_id: int, conn = Depends(db.get_connection)):
    
    grade_types = await grade_repository.get_grade_types_from_db(class_id, conn)

    return {"content": grade_types}

@router.get("/api/classes/{class_id}/{type_name}/assessments")
async def get_assessments(class_id: int, type_name: str, conn = Depends(db.get_connection)):

    assessments = await grade_repository.get_assessments(class_id, type_name, conn)

    return {"content": assessments}

@router.post("/api/grade_types")
async def insert_grade_type(grade_type: GradeType, conn = Depends(db.get_connection)):

    id = await grade_repository.insertDB_grade_type(grade_type, conn)

    return {"content": id} 

@router.delete("/api/classes/{class_id}/grade_types/{type_id}")
async def delete_grade_type_id(class_id: int, type_id: int, conn = Depends(db.get_connection)):
    res = await grade_repository.deleteDB_grade_type(class_id, type_id, conn)
    
    print(res)
    if res:
        return {"message": "grade type successfully deleted."}
    
    return {"message": "grade type doesn't exist."}