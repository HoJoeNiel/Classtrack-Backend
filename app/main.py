from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import dummy
from app.api.endpoints import auth_endpoint, class_endpoint
from app.core.database import Database
import asyncpg


@asynccontextmanager
async def lifespan(app: FastAPI):
	# Initialize database
	await Database.initialize()

	yield

	# Shutdown
	await Database.close_all()

app = FastAPI(lifespan=lifespan)


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

@app.get("/")
async def root():
	print("holy shit")
	return "Try using the dummy api! E.g. /dummy/luis"