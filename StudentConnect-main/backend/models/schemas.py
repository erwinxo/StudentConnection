from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostType(str, Enum):
    notes = "notes"
    jobs = "jobs"
    threads = "threads"

# User Models
class UserBase(BaseModel):
    email: EmailStr
    username: str
    name: str
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Post Models
class PostBase(BaseModel):
    title: str
    content: str
    post_type: PostType
    tags: Optional[List[str]] = []

class NotesPost(PostBase):
    document_url: Optional[str] = None
    document_name: Optional[str] = None

class JobsPost(PostBase):
    job_link: str
    company: Optional[str] = None
    location: Optional[str] = None

class ThreadsPost(PostBase):
    pass

class PostCreate(BaseModel):
    title: str
    content: str
    post_type: PostType
    tags: Optional[List[str]] = []
    document_url: Optional[str] = None
    document_name: Optional[str] = None
    job_link: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None

class PostResponse(PostBase):
    id: str
    author_id: str
    author_name: str
    author_username: str
    author_profile_picture: Optional[str] = None
    document_url: Optional[str] = None
    document_name: Optional[str] = None
    job_link: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    comments_count: int = 0
    created_at: datetime
    updated_at: datetime

# Comment Models
class CommentBase(BaseModel):
    content: str
    parent_comment_id: Optional[str] = None

class CommentCreate(CommentBase):
    post_id: str

class CommentResponse(CommentBase):
    id: str
    post_id: str
    author_id: str
    author_name: str
    author_username: str
    author_profile_picture: Optional[str] = None
    replies: List["CommentResponse"] = []
    created_at: datetime
    updated_at: datetime

# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
