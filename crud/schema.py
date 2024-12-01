from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    project_id: int

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    project_id: int | None = None
