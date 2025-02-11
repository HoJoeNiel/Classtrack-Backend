import firebase_admin 
from firebase_admin import auth, credentials
from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer


cred = credentials.Certificate("path")
firebase_admin.initialize_app(cred)

security = HTTPBearer()

async def verify_firebase_token(token: str = Security(security)):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return HTTPException(status_code=401, detail="Invalid Token")
    
    