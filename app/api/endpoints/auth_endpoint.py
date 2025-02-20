from app.core.security import verify_firebase_token
from app.core.database import get_connection
from fastapi import APIRouter, Depends

router = APIRouter()

async def verify_user(decoded_token: dict = Depends(verify_firebase_token), conn=Depends(get_connection)):

    uid = decoded_token["uid"] 
    email = decoded_token["email"]
    print(decoded_token)
    
    query = "SELECT * FROM professors WHERE uid = $1;"
    user = await conn.fetchrow(query, uid)

    if not user:
        insert_query = "INSERT INTO professors (uid, email) VALUES ($1, $2);"
        user = await conn.fetchrow(insert_query, uid, email)

    return {"Message": "User verified", "user_id":user["id"]}

@router.get("/test/test-auth")
async def test_auth(decoded_token: dict = Depends(verify_firebase_token)):
    return {"message": decoded_token}