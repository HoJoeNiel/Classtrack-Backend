from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import dummy
# from app.api.endpoints import auth
from app.core.database import Database



@asynccontextmanager
async def lifespan(app: FastAPI):
	# Initialize database
	await Database.initialize()

	yield

	# Shutdown
	await Database.close_all()

app = FastAPI(lifespan=lifespan)

# Using the endpoint defind in dummy
app.include_router(dummy.router)
# app.include_router(auth.router)

@app.get("/")
async def root():
	return "Try using the dummy api! E.g. /dummy/luis"