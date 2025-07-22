from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Basic Health Check")
async def health():
    return {"status": "ok"}
