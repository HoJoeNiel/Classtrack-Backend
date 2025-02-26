import asyncpg
from app.db.models.attendance_model import AttendanceModel, AttendanceDate, AttendanceRecord, AttendanceRecordsList

# Get all attendance dates for a class
async def get_attendance_dates(conn: asyncpg.Connection, class_id: int):
    return await conn.fetch("SELECT * FROM attendance_dates WHERE class_id = $1;", class_id)

# Get a specific attendance date
# added 'class_id' to avoid argument mismatch as endpoint calls for 'class_id'
async def get_attendance_date(conn: asyncpg.Connection, class_id: int, dates_id: int):
    return await conn.fetchrow("SELECT * FROM attendance_dates WHERE class_id = $1 AND date_id = $2;", class_id, dates_id)

# Insert a new attendance date
# added 'class_id' to avoid argument mismatch as endpoint calls for 'class_id'
async def insert_attendance_date(conn: asyncpg.Connection, class_id: int, new_date: AttendanceDate):
    return await conn.fetchval("INSERT INTO attendance_dates (class_id, date_id, attendance_date) VALUES ($1, $2, $3) RETURNING date_id;", class_id, new_date.date_id, new_date.attendance_date)

# Delete an attendance date
# added 'class_id' to avoid argument mismatch as endpoint calls for 'class_id'
async def delete_attendance_date(conn: asyncpg.Connection, class_id: int, dates_id: int):
    return await conn.execute("DELETE FROM attendance_dates WHERE class_id = $1 AND date_id = $2;", class_id, dates_id)

# Get all attendance records for a class
async def get_attendance_records(conn: asyncpg.Connection, date_id: int):
    records = await conn.fetch("SELECT * FROM attendance_records WHERE date_id = $1;", date_id)
    return AttendanceRecordsList(records=[AttendanceRecord(**dict(record)) for record in records])

# Insert a new attendance record
async def insert_attendance_record(conn: asyncpg.Connection, record: AttendanceRecord):
    return await conn.execute("INSERT INTO attendance_records (record_id, student_number, date_id, status) VALUES ($1, $2, $3, $4);",record.record_id, record.student_number, record.date_id, record.status)

# Update attendance record using record_id 
# added 'date_id' to avoid argument mismatch as endpoint calls for 'date_id'
async def update_attendance_record(conn: asyncpg.Connection, date_id: int, record: AttendanceRecord):
    return await conn.execute("UPDATE attendance_records SET status = $1 WHERE class_id = $2 AND record_id = $3;",record.status, date_id, record.record_id)

# Delete attendance record using record_id
async def delete_student_from_class(conn: asyncpg.Connection, record_id: int):
    result = await conn.execute("DELETE FROM attendance_records WHERE record_id = $1;",record_id)
    return result == "DELETE 1"  # Returns True if a record was deleted