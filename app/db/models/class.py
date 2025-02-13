from pydantic import BaseModel

class Class(BaseModel):
    id: str
    prof_id: str
    class_id: str
    class_size: int
    schedule: str
    section: str
    subject: str
    subject_code: str
