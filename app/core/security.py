import firebase_admin 
from firebase_admin import auth, credentials
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CRED_PATH").replace("\\n", "\n"))
firebase_admin.initialize_app(cred)

security = HTTPBearer()

async def verify_firebase_token(token: str = Security(security)):
    try:
        # Attempt to verify the Firebase ID token
        decoded_token = auth.verify_id_token(token.credentials, clock_skew_seconds=10)
        print("Decoded Token:", decoded_token)  # Check the decoded token
        return decoded_token
    except Exception as e:
        # Print error message to debug
        print("Token verification failed:", str(e))
        raise HTTPException(status_code=401, detail="Invalid Token")
    

# user =  auth.create_user(email="nig@gmail.com", password="test12345")
# customtoken = auth.create_custom_token("idf7PerAlzQffdBhC7zg2cFoCU12").decode("utf-8")
