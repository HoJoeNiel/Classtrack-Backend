import firebase_admin 
from firebase_admin import auth, credentials
from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os
import json
import base64

load_dotenv()

firebase_base64 = os.environ.get("CREDENTIALS_FIREBASE_AUTH")

if firebase_base64:

    firebase_json =  json.loads(base64.b64decode(firebase_base64))

    cred = credentials.Certificate(firebase_json)
    firebase_admin.initialize_app(cred)
else:
    raise ValueError("CREDENTIALS_FIREBASE_AUTH is not found in environment variables")

security = HTTPBearer()

async def verify_firebase_token(token: str = Security(security)):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return HTTPException(status_code=401, detail="Invalid Token")
    

user =  auth.create_user(email="anothertestuser@gmail.com", password="test12345")
customtoken = auth.create_custom_token(user.uid)
print(customtoken)