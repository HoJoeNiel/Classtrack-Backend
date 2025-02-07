from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_dummy():
	res = client.get("/dummy/Luis")
	assert res.status_code == 200 # status ok
	assert res.read().decode().replace('"', "") == "Hello Dummy Luis"

def test_dummyson():
	res = client.get("/dummyson/Luis")
	assert res.status_code == 200 # status ok
	assert res.json() == {"msg": "Hello Dummy Luis"}