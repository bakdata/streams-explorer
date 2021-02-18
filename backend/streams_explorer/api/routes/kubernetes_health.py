from fastapi import APIRouter

router = APIRouter()


@router.get("/live", status_code=200)
async def live():
    return {"status": "UP"}


@router.get("/ready", status_code=200)
async def ready():
    return {"ready": True}
