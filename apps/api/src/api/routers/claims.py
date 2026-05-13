from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_claims():
    return {"message": "TODO: implement claims endpoints"}
