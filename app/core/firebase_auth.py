import firebase_admin 
from firebase_admin import auth, credentials
from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os
import json
import base64

load_dotenv()

firebase_json = os.getenv("FIREBASE_JSON")
cred = credentials.Certificate(firebase_json)
firebase_admin.initialize_app(cred)

security = HTTPBearer()

async def verify_firebase_token(token: str = Security(security)):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return HTTPException(status_code=401, detail="Invalid Token")
    

# user =  auth.create_user(email="dan@gmail.com", password="test12345")
customtoken = auth.create_custom_token("Ps9FnhDzfGRj1elCEfSbIe8b0Sj1")
print(customtoken)