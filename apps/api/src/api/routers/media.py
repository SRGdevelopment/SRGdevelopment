from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_media():
    return {"message": "TODO: implement media endpoints"}
