from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from datetime import datetime

from schema.object_id import PyObjectId
from core.enums.role import UserRole

import re


# ------------- BASE CLASS FOR USER --------------
class UserBase(BaseModel):
    email : EmailStr = Field(..., description = "User's email (must be UNIQUE)")
    name  : str      = Field(..., min_length = 2, max_length = 100)
    role  : UserRole = UserRole.PASSENGER

    model_config = ConfigDict(use_enum_values = True)

    @field_validator("email")
    @classmethod
    def check_email(cls, v : str) -> str:
        return v.lower().strip() 


# ------------- CLASSES FOR HTTP HANDLERS --------
class UserCreate(UserBase):
    password : str = Field(min_length = 8, max_length = 64)

    @field_validator("password")
    @classmethod
    def check_password(cls, v : str) -> str:
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a number")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain a capital letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain a lowercase letter")
        return v


class UserLogin(BaseModel):
    email : EmailStr
    password : str



class UserResponse(UserBase):

    id : PyObjectId = Field(alias = "_id", default_factory = PyObjectId)

    is_active:   bool = True
    is_verified: bool = False

    created_at : datetime = Field(default_factory = datetime.now)
    updated_at : datetime = Field(default_factory = datetime.now)

    @field_validator("id", mode = "before")
    @classmethod
    def validate_id(cls, v : str) -> PyObjectId:
        if isinstance(v, str):
            return PyObjectId(v)
        return v

    model_config = ConfigDict(populate_by_name=True,
                              arbitrary_types_allowed=True)


# --------------- CLASSES FOR MONGODB -------------
class UserInDB(UserResponse):
    hashed_password : str 