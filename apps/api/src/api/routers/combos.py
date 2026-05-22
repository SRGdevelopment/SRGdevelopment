from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_combos():
    return {"message": "TODO: implement combos endpoints"}
