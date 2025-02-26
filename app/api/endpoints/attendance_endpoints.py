import asyncpg
from fastapi import APIRouter, Depends, HTTPException
import app.core.database as db
from app.core.security import verify_firebase_token
from app.db.models.attendance_model import AttendanceDate, AttendanceRecord, AttendanceRecordsList
import app.db.repositories.attendance_repository as attendance_repository

router = APIRouter()

# Get all attendance dates for a class
@router.get("/api/classes/{class_id}/attendance_dates")
async def get_attendance_dates(class_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    res = await attendance_repository.get_attendance_dates(conn, class_id)
    return {"attendance_dates": res}

# Add a new attendance date
@router.post("/api/classes/{class_id}/attendance_dates")
async def add_attendance_date(class_id: int, date_body: AttendanceDate, conn: asyncpg.Connection = Depends(db.get_connection)):
    res = await attendance_repository.insert_attendance_date(conn, class_id, date_body)
    return {"attendance_date_id": res}

# Delete an attendance date
@router.delete("/api/classes/{class_id}/attendance_dates/{dates_id}")
async def delete_attendance_date(class_id: int, dates_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    date_data = await attendance_repository.get_attendance_date(conn, class_id, dates_id)

    if not date_data:
        raise HTTPException(status_code=404, detail="Attendance date not found")
    
    await attendance_repository.delete_attendance_date(conn, class_id, dates_id)
    return {"attendance_date": date_data}

# Get attendance records
@router.get("/api/classes/{date_id}/attendance_records")
async def get_attendance_records(date_id: int, conn: asyncpg.Connection = Depends(db.get_connection)):
    res: AttendanceRecordsList = await attendance_repository.get_attendance_records(conn, date_id) 
    return res.model_dump()

# Update attendance record using record_id 
# added 'date_id' to avoid argument mismatch as endpoint calls for 'date_id'
@router.put("/api/classes{class_id}/attendance_records")
async def update_attendance_record(class_id: int, record: AttendanceRecordsList, conn: asyncpg.Connection = Depends(db.get_connection)):
    res =  await attendance_repository.update_attendance_record(conn, record, class_id)
    return res