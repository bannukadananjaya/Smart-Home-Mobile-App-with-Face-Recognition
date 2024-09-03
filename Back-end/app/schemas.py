from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str



class LogBase(BaseModel):
    user_id: int
    entry_time: datetime
    date: datetime

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int

    class Config:
        orm_mode = True


# Define a model for the response
class UserIdResponse(BaseModel):
    id: str

# class Log(BaseModel):
#     id: int
#     user_id: int
#     username: str
#     entry_time: datetime
#     date: str

#     class Config:
#         orm_mode = True