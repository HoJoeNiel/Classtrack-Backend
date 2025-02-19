from fastapi.testclient import TestClient
from app.main import app
import requests
from firebase_admin import auth

client = TestClient(app)

def exchange_custom_token(custom_token, key):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={key}"
    payload = {
        "token": custom_token,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

def test_auth_endpoint():

    key = "AIzaSyCJD9sLFzbYHSbQ_At08zMYyJXvi2w_lgI"

    custom_token = auth.create_custom_token("idf7PerAlzQffdBhC7zg2cFoCU12").decode("utf-8")

    # Print the token to use in the next step
    print("Custom Token:", custom_token)


    id_token_response = exchange_custom_token(custom_token, key)
    id_token = id_token_response.get("idToken")
    print("Firebase ID Token:", id_token)


    headers = {
        "Authorization": f"Bearer {id_token}"
    }
    
    response = client.get("/test/test-auth", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()