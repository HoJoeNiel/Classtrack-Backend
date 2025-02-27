from pydantic import BaseModel

class GradeType(BaseModel):
    class_id: int
    type_name: str