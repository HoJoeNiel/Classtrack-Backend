from pydantic import BaseModel



class AssessmentModel(BaseModel):
    assessment_name: str
    total_items: int


