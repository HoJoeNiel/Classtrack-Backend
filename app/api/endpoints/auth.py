from app import core
from app.core.firebase_auth import verify_firebase_token
from app.core.database import get_db
from fastapi import APIRouter, Depends
import asyncpg

router = APIRouter()

async def verify_user(decoded_token: dict = Depends(verify_firebase_token), db=Depends(get_db)):

    user_id = decoded_token["uid"]
    username = decoded_token["username"] #for prof credentials, not sure yet the final info of the professors.

    query = "SELECT id FROM users WHERE firebase_uid = $1"
    user = await db.fetchrow(query, user_id)

    if not user:
        insert_query = "INSERT INTO users (firebase_uid, email) VALUES ($1, $2) RETURNING id"
        user = await db.fetchrow(insert_query, user_id)

    return {"Message": "User verified", "user_id":user["id"]}

@router.get("/test-auth")
async def test_auth(decoded_token: dict = Depends(verify_firebase_token)):
    return {"message": "Authenticated successfully", "user": decoded_token}