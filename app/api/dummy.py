from fastapi import APIRouter

router = APIRouter()


@router.get("/dummy/{name}")
async def get_dummy(name: str):
	return f"Hello Dummy {name}"

@router.get("/dummyson/{name}/")
async def get_dummy_json(name):
	return {"msg": f"Hello Dummy {name}"}