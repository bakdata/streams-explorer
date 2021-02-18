from fastapi import APIRouter

router = APIRouter()


@router.get("", status_code=200, include_in_schema=False)
async def ready():
    return {"ready": True}
