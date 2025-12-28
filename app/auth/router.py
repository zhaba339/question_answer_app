from fastapi import APIRouter, Response, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from app.auth.schemas import UserLoginSchema
from app.auth.security import security, config

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)




@router.post("/login")
async def login(creds: UserLoginSchema, response: Response):
    if creds.username == "admin" and creds.password == "admin":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@router.post("/register")
async def register():
    pass


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"protected": True}
