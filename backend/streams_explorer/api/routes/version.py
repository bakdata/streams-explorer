from fastapi import APIRouter

from streams_explorer import __version__

router = APIRouter()


@router.get("", status_code=200)
async def version():
    return __version__
