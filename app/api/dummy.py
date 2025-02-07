from fastapi import APIRouter

router = APIRouter()


@router.get("/dummy/{name}")
async def get_dummy(name: str):
  return f"Hello Dummy {name}"

