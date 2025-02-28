from pydantic import BaseModel
from typing import List

class GradeType(BaseModel):
    class_id: int
    type_name: str

class AssessmentModel(BaseModel):
    assessment_name: str
    total_items: int

class ScoreUpdateModel(BaseModel):
    student_number: str
    assessment_id: int
    score: int

class ScoreList(BaseModel):
    scores: List[ScoreUpdateModel]
