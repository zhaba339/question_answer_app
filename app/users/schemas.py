from pydantic import BaseModel, ConfigDict, UUID4


class BaseUserSchema(BaseModel):
    pass

    class Config:
        model_config = ConfigDict(from_attributes = True)

class UserSchema(BaseUserSchema):
    id: int
    login: str
    password: str
