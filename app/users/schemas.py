from pydantic import BaseModel, ConfigDict


class BaseUserSchema(BaseModel):
    pass

    class Config:
        model_config = ConfigDict(from_attributes = True)

class UserSchema(BaseUserSchema):
    id: int
    user_id: int
    login: str
    password: str
