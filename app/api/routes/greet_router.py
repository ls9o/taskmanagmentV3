from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from app.config import settings

router = APIRouter()


@router.get("/")
async def value_verify():
    return JSONResponse(
        content={
            "app_name": settings.app_name,
            "verify_message": settings.verify_message,
        }
    )
