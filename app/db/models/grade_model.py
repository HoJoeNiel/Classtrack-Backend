from pydantic import BaseModel
from typing import List


class AssessmentModel(BaseModel):
    assessment_name: str
    total_items: int


class ScoreUpdateModel(BaseModel):
    student_number: str
    assessment_id: int
    score: int

class ScoreList(BaseModel):
    scores: List[ScoreUpdateModel]


