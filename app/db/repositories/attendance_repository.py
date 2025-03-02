import asyncpg
from app.db.models.attendance_model import AttendanceModel, AttendanceDate, AttendanceRecord, AttendanceRecordsList
from fastapi import Depends, HTTPException
import app.core.database as db

# Get all attendance dates for a class
async def get_attendance_dates(conn: asyncpg.Connection, class_id: int):
    return await conn.fetch("SELECT * FROM attendance_dates WHERE class_id = $1;", class_id)

# Get a specific attendance date
async def get_attendance_date(conn: asyncpg.Connection, class_id: int, dates_id: int):
    return await conn.fetchrow("SELECT * FROM attendance_dates WHERE class_id = $1 AND date_id = $2;", class_id, dates_id)

# Insert a new attendance date
async def insert_attendance_date(conn: asyncpg.Connection, class_id: int, new_date: AttendanceDate):
    await attendance_record_trigger(conn)
    return await conn.fetchval(
        "INSERT INTO attendance_dates (class_id, date_id, attendance_date) VALUES ($1, $2, $3) RETURNING date_id;",
        class_id, new_date.date_id, new_date.attendance_date
    )

# Delete an attendance date
async def delete_attendance_date(conn: asyncpg.Connection, class_id: int, dates_id: int):
    return await conn.execute("DELETE FROM attendance_dates WHERE class_id = $1 AND date_id = $2;", class_id, dates_id)

# Get all attendance records for a class
async def get_attendance_records(conn: asyncpg.Connection, date_id: int):
    query = """
        SELECT s.student_number, 
               s.first_name || ', ' || s.last_name AS name, 
               ar.record_id, 
               ar.date_id, 
               COALESCE(ar.record_status, 'not recorded') AS record_status
        FROM students s
        LEFT JOIN attendance_records ar 
        ON s.student_number = ar.student_number AND ar.date_id = $1
        WHERE s.class_id = (SELECT class_id FROM attendance_dates WHERE date_id = $1);
    """
    return await conn.fetch(query, date_id)

# Insert a new attendance record
async def insert_attendance_record(conn: asyncpg.Connection, record: AttendanceRecord):
    await students_attendance_trigger(conn)
    return await conn.execute("INSERT INTO attendance_records (record_id, student_number, date_id, status) VALUES ($1, $2, $3, $4);",
                              record.record_id, record.student_number, record.date_id, record.record_status)

# Update attendance record using record_id 
async def update_attendance_record(conn: asyncpg.Connection, date_id: int, record: AttendanceRecord):
    return await conn.execute("UPDATE attendance_records SET status = $1 WHERE date_id = $2 AND record_id = $3;",
                              record.record_status, date_id, record.record_id)

# Delete attendance record using record_id
async def delete_student_from_class(conn: asyncpg.Connection, record_id: int):
    result = await conn.execute("DELETE FROM attendance_records WHERE record_id = $1;", record_id)
    return result == "DELETE 1"  

# Trigger to set default status to 'absent' when a new attendance date is added
async def attendance_record_trigger(conn: asyncpg.Connection = Depends(db.get_connection)):
    function_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_proc WHERE proname = 'insert_default_attendance'
        );
    """)

    if not function_exists:
        await conn.execute("""
            CREATE OR REPLACE FUNCTION insert_default_attendance()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO attendance_records (student_number, date_id, record_status)
                SELECT s.student_number, NEW.date_id, 'absent'
                FROM students s
                WHERE s.class_id = NEW.class_id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

    trigger_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = 'auto_insert_attendance'
        );
    """)

    if not trigger_exists:
        await conn.execute("""
            CREATE TRIGGER auto_insert_attendance
            AFTER INSERT ON attendance_dates
            FOR EACH ROW EXECUTE FUNCTION insert_default_attendance();
        """)

# Trigger function to auto-fill attendance records for new students
async def students_attendance_trigger(conn: asyncpg.Connection = Depends(db.get_connection)):
    function_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_proc WHERE proname = 'add_default_attendance'
        );
    """)

    if not function_exists:
        await conn.execute("""
            CREATE OR REPLACE FUNCTION add_default_attendance()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO attendance_records (student_number, date_id, record_status)
                SELECT NEW.student_number, a.date_id, 'absent'
                FROM attendance_dates a
                WHERE a.class_id = NEW.class_id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

    trigger_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = 'auto_add_attendance'
        );
    """)

    if not trigger_exists:
        await conn.execute("""
            CREATE TRIGGER auto_add_attendance
            AFTER INSERT ON students
            FOR EACH ROW EXECUTE FUNCTION add_default_attendance();
        """)
