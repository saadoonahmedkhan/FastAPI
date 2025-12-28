from datetime import datetime
from typing import Optional , Literal
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    username: str
    class Config():
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config():
        from_attributes = True

class User_login(BaseModel):
    email: EmailStr
    password: str


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    owner: UserOut
    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token:str 
    token_type:str 

class Token_Data(BaseModel):
    user_id:str


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class Post_with_Votes(BaseModel):
    post: Post
    votes: int