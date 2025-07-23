from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Basic Health Check")
def health():
    return {"status": "ok"}
