import asyncpg
from fastapi import FastAPI
<<<<<<< HEAD
from contextlib import asynccontextmanager

DATABASE_URL= ("Url to our database")

@asynccontextmanager
=======
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
user = os.getenv("POSTGRES_USER")
password= os.getenv("POSTGRES_PASSWORD")

>>>>>>> 4c42a090702768c5984ca9e9d422d9d1db54646f
async def lifespan(app: FastAPI):
	print("connecting to db")
	db_pool = await asyncpg.create_pool(database="classtrack", user=user, password=password)
	app.state.db_pool = db_pool
	print("dp_pool", "connected!")
	yield
	await db_pool.close()    

app = FastAPI(lifespan=lifespan)

async def get_db():
	async with app.state.db_pool.acquire() as connection:
		yield connection


class Database:
	_pool = None

	@classmethod
	async def initialize(cls, max_retries=5, base_delay=0.5):
		for attempt in range(1, max_retries + 1): # backoff strategy
			try:
				cls._pool = await asyncpg.create_pool(
					database="classtrack",
					user=user,
					password=password,
					)
		
				print("Database initialized successfully.")
				return
			
			except Exception as e:
				print(f"Database initialization failed (attempt {attempt}): {e}")

				if attempt < max_retries:
					delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff
					print(f"Retrying in {delay} seconds.")
					await asyncio.sleep(delay)

				else: # no more retries
					print("Max retries reached. Could not connect to database.")
					raise

				
	@classmethod 
	async def get_connection(cls):
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		
		return await cls._pool.acquire()
	
	@classmethod
	async def release_connection(cls, conn):
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		elif conn is None:
			raise Exception("Conn cannot be None.")
		
		await cls._pool.release(conn)

	@classmethod
	async def close_all(cls):
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		
		await cls._pool.close()