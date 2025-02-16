import asyncpg
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
user = os.getenv("POSTGRES_USER")
password= os.getenv("POSTGRES_PASSWORD")

if not user or not password:
	raise ValueError("POSTGRES_USER and POSTGRES_PASSWORD must be set in the .env file.")

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
		""" Returns a connection from the connection pool. """
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		
		return await cls._pool.acquire()
	
	@classmethod
	async def release_connection(cls, conn):
		""" Releases a connection back to the pool. """
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		elif conn is None:
			raise Exception("Conn cannot be None.")
		
		await cls._pool.release(conn)

	@classmethod
	async def close_all(cls):
		"""Close all connection in the pool."""
		if cls._pool is None:
			raise Exception("Database not initialized. Call Database.initialize() first.")
		
		await cls._pool.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
	"""Handles FastAPI startup and shutdown events"""

	print("Connecting to the database...")
	await Database.initialize()
	print("Database connected!")

	yield

	print("Shutting down database...")
	await Database.close_all()    
	print("Database connection closed.")

app = FastAPI(lifespan=lifespan)


async def get_connection():
	"""Dependency to get a database connection."""
	conn = await Database.get_connection()

	try:
		yield conn

	finally:
		await Database.release_connection(conn)	
