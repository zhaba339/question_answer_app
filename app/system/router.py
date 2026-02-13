from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/health")
async def healthcheck():
    return {"message": "Здесь будет проверка системы"}
