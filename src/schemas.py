from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  #sql -> Pydantic conversion

class PostCreate(BaseModel):
    title : str
    content : str

class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    created_at : datetime
    author_id : int

    class Config:
        from_attributes = True

class PostWithAuthor(PostResponse):
    author : UserResponse

class CommentCreate(BaseModel):
    body : str

class CommentResponse(BaseModel):
    id : int
    body : str
    created_at : datetime
    post_id : int
    author_id : int

    class Config:
        from_attributes = True