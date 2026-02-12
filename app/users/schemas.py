from pydantic import BaseModel, ConfigDict, UUID4


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseUserSchema):
    id: int
    login: str
    password: str
    is_admin: bool


class UserRegisterSchema(BaseUserSchema):
    login: str
    password: str


class UserLoginSchema(BaseUserSchema):
    login: str
    password: str