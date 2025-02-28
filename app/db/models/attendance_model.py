import datetime
from typing import List
from pydantic import BaseModel

class AttendanceModel(BaseModel):
    student_id:int
    class_id: int
    date_id: int

class AttendanceDate(BaseModel):
    date_id: int
    attendance_date: datetime.date

class AttendanceRecord(BaseModel):
    record_id: int
    student_number: str
    date_id: int
    record_status: str

class AttendanceRecordsList(BaseModel):
    records: List[AttendanceRecord]