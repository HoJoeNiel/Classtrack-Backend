from pydantic import BaseModel

class ClassModel(BaseModel):
    prof_id: str
    class_size: int
    schedule: str
    section: str
    subject_name: str
    subject_code: str

