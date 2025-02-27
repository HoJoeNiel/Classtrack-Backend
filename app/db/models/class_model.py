from typing import List
from pydantic import BaseModel, EmailStr

class ClassModel(BaseModel):
    prof_id: str
    class_size: int
    schedule: str
    section: str
    subject_name: str
    subject_code: str

class Students(BaseModel):
    student_number:str
    class_id:int
    first_name:str
    last_name: str
    course: str
    email: EmailStr

class Content(BaseModel):
    content: List[Students]