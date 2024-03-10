from fastapi import APIRouter

router = APIRouter()

@router.get("/senror")
async def read_file():
    return [{"usernadme"}]