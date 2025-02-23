from pydantic import BaseModel



class AssessmentModel(BaseModel):
    grade_id: int
    class_id: int
    grade_type_id: int
    assessment_name: str


