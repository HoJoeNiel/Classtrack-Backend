from app.core.security import verify_firebase_token
from app.core.database import get_connection
from fastapi import APIRouter, Depends

router = APIRouter()

async def verify_user(decoded_token: dict = Depends(verify_firebase_token), conn=Depends(get_connection)):
    try:
        uid = decoded_token["uid"] 
        email = decoded_token["email"]
        print(decoded_token)
        
        full_name = decoded_token["name"].split(", ")
        print(full_name)
        first_name = full_name[1]
        last_name = full_name[0]

        # first_name = "Fuck"
        # last_name = "THIS"
        query = "SELECT * FROM professors WHERE uid = $1;"
        user = await conn.fetchrow(query, uid)

        if not user:
            insert_query = "INSERT INTO professors (uid, first_name, last_name, email) VALUES ($1, $2, $3, $4) RETURNING *;"
            user = await conn.fetchrow(insert_query, uid, first_name, last_name, email)

        return {"Message": "User verified", "user_id":user["id"]}
    except Exception as e:
        print(f"Failed to verify user: {e}")

@router.get("/test/test-auth")
async def test_auth(decoded_token: dict = Depends(verify_firebase_token)):
    return {"message": decoded_token}