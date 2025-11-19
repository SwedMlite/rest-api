from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ConfiguredBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(ConfiguredBase):
    first_name: str = Field(..., min_length=1, max_length=120, alias="firstName")
    last_name: str = Field(..., min_length=1, max_length=120, alias="lastName")
    birth_date: date = Field(..., alias="birthDate")
    email: EmailStr
    active: bool = True
    role: UserRole


class UserCreate(UserBase):
    pass


class UserUpdate(ConfiguredBase):
    first_name: Optional[str] = Field(None, min_length=1, max_length=120, alias="firstName")
    last_name: Optional[str] = Field(None, min_length=1, max_length=120, alias="lastName")
    birth_date: Optional[date] = Field(None, alias="birthDate")
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserOut(ConfiguredBase):
    id: int
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    birth_date: date = Field(..., alias="birthDate")
    email: EmailStr
    active: bool
    role: UserRole
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class PostBase(ConfiguredBase):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    link: Optional[str] = Field(None, max_length=512)
    user_id: int = Field(..., alias="userId")


class PostCreate(PostBase):
    pass


class PostUpdate(ConfiguredBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, min_length=1)
    link: Optional[str] = Field(None, max_length=512)
    user_id: Optional[int] = Field(None, alias="userId")


class PostOut(ConfiguredBase):
    id: int
    title: str
    body: str
    link: Optional[str] = None
    user_id: int = Field(..., alias="userId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class CommentBase(ConfiguredBase):
    body: str = Field(..., min_length=1)
    user_id: int = Field(..., alias="userId")
    post_id: int = Field(..., alias="postId")


class CommentCreate(CommentBase):
    pass


class CommentUpdate(ConfiguredBase):
    body: Optional[str] = Field(None, min_length=1)
    user_id: Optional[int] = Field(None, alias="userId")
    post_id: Optional[int] = Field(None, alias="postId")


class CommentOut(ConfiguredBase):
    id: int
    body: str
    user_id: int = Field(..., alias="userId")
    post_id: int = Field(..., alias="postId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
