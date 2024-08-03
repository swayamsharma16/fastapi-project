from dataclasses import Field
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Annotated, Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    

class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


    class config:
        orm: True

class PostOut(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(ge=1)]


    