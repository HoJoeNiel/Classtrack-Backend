import asyncpg
from fastapi import FastAPI
from contextlib import asynccontextmanager

DATABASE_URL= ("Url to our database")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    app.state.db_pool = db_pool
    yield
    await db_pool.close()    

app = FastAPI(lifespan=lifespan)
    

async def get_db():
    async with app.state.db_pool.acquire() as connection:
        yield connection