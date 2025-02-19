import pytest
from fastapi.testclient import TestClient
from app.main import app
import requests
from firebase_admin import auth

client = TestClient(app)


@pytest.fixture
def fake_token():
    """Return Fake firebase token for testing"""
    return "Bearer eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiNGE2M2I5MDE0Yzg0MmFmMGQyNDZjMjkxMGQ1OTQ0YjJmNjJjZjVjZiJ9.eyJpc3MiOiAiZmlyZWJhc2UtYWRtaW5zZGstOTBlYXZAY2xhc3N0cmFjay1yZW1ha2UuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAic3ViIjogImZpcmViYXNlLWFkbWluc2RrLTkwZWF2QGNsYXNzdHJhY2stcmVtYWtlLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwgImF1ZCI6ICJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsICJ1aWQiOiAiWVdOcmlVdHlGemVJeDRIMWV2bDNicDRqdDVlMiIsICJpYXQiOiAxNzM5MzYxNDEwLCAiZXhwIjogMTczOTM2NTAxMH0.FKgpg6CvWqAT_KBAzyrF1kjg4XexoPJi3dIuwPqLHEh_wxFmO0ivaSuTYOfZdpI5xIvEiE4Wt9b341SuG30ugkXTgh0ZLKSG20_MzRg5DeHMB4JNliYBInXffOD_f3ln789VC6zCho-yqJeOin7_faWixEhsbA569s8wgf43qBcuDGVPfncXWmcHqjoUDAYBzcoqylLZ9L4JYUW5kBQ4kAxXWJtpGy4A8387XOXgVcy8lnW0_KHBkrbsEhM3G0VzEdVpxbTHr_Wp0Kd6ualT9nlo6CKPoJgz-1C-Np0IoZVhK5d9i_Dg0bPuqekt90A2IEmmqCwFC8XKlSzz_1HmZg"

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

