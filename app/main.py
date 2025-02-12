from fastapi import FastAPI
from app.api import dummy
from app.api.endpoints import auth

app = FastAPI()

# Using the endpoint defind in dummy
app.include_router(dummy.router)
app.include_router(auth.router)

@app.get("/")
async def root():
	return "Try using the dummy api! E.g. /dummy/luis"