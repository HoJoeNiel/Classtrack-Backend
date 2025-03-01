import asyncpg
from fastapi import APIRouter, Body, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
import app.db.repositories.grade_repository as grade_repository
from app.db.repositories import class_repository
from app.db.models.grade_model import AssessmentModel, ScoreList, GradeType
from typing import Annotated

router = APIRouter()


@router.get("/api/classes/{class_id}/grade_types")
async def get_grade_types(class_id: int, conn = Depends(db.get_connection)):
    
    grade_types = await grade_repository.get_grade_types_from_db(class_id, conn)

    return {"content": grade_types}

@router.get("/api/classes/{class_id}/{grade_type_id}/assessments")
async def get_assessments(class_id: int, grade_type_id: int, conn = Depends(db.get_connection)):

    assessments = await grade_repository.get_assessments(class_id, grade_type_id, conn)

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

@router.post("/api/classes/{class_id}/{grade_type_id}/assessments")
async def insert_assessment(assessment_model: Annotated[AssessmentModel, Body(embed=True)],
                            class_id: int,
                            grade_type_id: int, 
                            conn: asyncpg.Connection = Depends(db.get_connection)):
    await grade_repository.insert_assessment_to_db(conn, class_id, grade_type_id, assessment_model)

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


# New Endpoints, from jonel
@router.get("/api/grades/{class_id}")
async def get_grades_by_class(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    
    # Get all students from class
    try:
        students = await class_repository.get_students_from_classes_table(conn, class_id)
        students = [
            {
                "name": f"{student['last_name']}, {student['first_name']}",
                "student_number": student["student_number"],
                "grades": []
            }
            for student in students
        ]
        
    except Exception as e:
        print(f"Failed to get students: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get students: {str(e)}")
    
    print(students)
    
    # Get all grade_types in the class
    try:
        grade_types = await grade_repository.get_grade_types_from_db(class_id, conn)
        grade_types = [dict(i) for i in grade_types]

    except Exception as e:
        print(f"Failed to get grade_types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get grade types: {str(e)}")

    
    # Get all assessments and group them by their grade_type_id
    try:
        assessments = await conn.fetch(
            "SELECT assessment_id, grade_type_id from assessments WHERE class_id = $1",
            class_id
        )

        assesments_by_type = {}
        for assessment in assessments:
            g_type_id = assessment["grade_type_id"]
            assesments_by_type.setdefault(g_type_id, []).append(assessment["assessment_id"])
    
    except Exception as e:
        print(f"Failed to get assessments: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get assessments: {str(e)}")

    # Get all scores and put them in dictionary
    try:
        scores = await conn.fetch(
            "SELECT * FROM scores WHERE assessment_id = ANY($1)",
            [a["assessment_id"] for a in assessments]
        )


        scores_by_student = {}
        for score in scores:
            key = (score["student_number"], score["assessment_id"])
            scores_by_student[key] = score["score"]

    except Exception as e:
        print(f"Failed to get scores: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get scores: {str(e)}") 


    # Put scores on students
    for student in students:
        student_num = student["student_number"]
        grades = []

        for g_type in grade_types:
            g_type_id = g_type["grade_type_id"]
            assessment_ids = assesments_by_type.get(g_type_id, [])

            scores_list = [
                {"assessment_id": a_id, "score": scores_by_student.get((student_num, a_id), 0)}
                for a_id in assessment_ids
            ]

            grades.append({"type": g_type["type_name"], "scores": scores_list})

        student["grades"] = grades

    return students
  