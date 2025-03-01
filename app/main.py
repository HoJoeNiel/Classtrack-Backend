from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import dummy
from app.api.endpoints import auth_endpoint, class_endpoint, grade_endpoint, attendance_endpoint
from app.core.database import Database
from app.db.repositories.grade_repository import score_trigger, student_score_trigger 
from app.db.repositories.attendance_repository import attendance_record_trigger, students_attendance_trigger
import asyncpg
from fastapi.middleware.cors import CORSMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
	# Initialize database
	await Database.initialize()

	conn = await Database.get_connection()
	await score_trigger(conn)
	await student_score_trigger(conn)
	await students_attendance_trigger(conn)
	await attendance_record_trigger(conn)
	await conn.close()
	yield

	# Shutdown
	await Database.close_all()

app = FastAPI(lifespan=lifespan)

# TO CONNECT OUR BACKEND TO FRONTEND
app.add_middleware(
	CORSMiddleware,
	allow_origins = ["https://62f0-2405-8d40-444d-8cb2-b0d8-57b0-53c7-32c4.ngrok-free.app", "http://localhost:5173"], # React FrontEnd URL
	allow_credentials = True, 	
	allow_methods = ["*"], # Allow all HTTP request (GET, POST, PUT...)
	allow_headers = ["*"]  # Allow all headers like Authorization
)


# Error handler middlewares
@app.exception_handler(asyncpg.PostgresError)
async def database_exception_handler(request: Request, exc: asyncpg.PostgresError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

# Using the endpoint defind in dummy
app.include_router(dummy.router)
app.include_router(auth_endpoint.router)
app.include_router(class_endpoint.router)
app.include_router(grade_endpoint.router)
app.include_router(attendance_endpoint.router)

@app.get("/")
async def root():
	print("holy shit")
	return "Try using the dummy api! E.g. /dummy/luis"