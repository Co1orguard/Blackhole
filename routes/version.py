from fastapi import APIRouter

router = APIRouter()

@router.get("/version")
def read_root():
    return {"api_version": "1.0.0"}

