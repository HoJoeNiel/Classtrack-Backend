from app.core.security import verify_firebase_token
from app.core.database import get_connection
from fastapi import APIRouter, Depends

router = APIRouter()


async def verify_user(decoded_token: dict = Depends(verify_firebase_token), conn=Depends(get_connection)):

    uid = decoded_token["uid"]
    first_name = "testing"
    last_name = "testing"
    email = decoded_token["email"]
    print(decoded_token)
    
    query = "SELECT * FROM professors WHERE uid = $1;"
    user = await conn.fetchrow(query, uid)

    if not user:
        insert_query = "INSERT INTO professors (uid, first_name, last_name, email) VALUES ($1, $2, $3, $4) RETURNING *;"
        user = await conn.fetchrow(insert_query, uid, first_name, last_name, email)

    return user

@router.get("/test/test-auth")
async def test_auth(decoded_token: dict = Depends(verify_firebase_token)):
    return {"message": decoded_token}