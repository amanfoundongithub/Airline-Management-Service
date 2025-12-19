from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

from datetime import datetime

from schema.object_id import PyObjectId
from core.constants import UserRole


# ------------- BASE CLASS FOR USER --------------
class UserBase(BaseModel):
    email : EmailStr = Field(..., description = "User's email (must be UNIQUE)")
    name  : str      = Field(..., min_length = 2, max_length = 100)
    role  : UserRole = UserRole.PASSENGER

    model_config = ConfigDict(use_enum_values = True)

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v : str) -> str:
        return v.lower().strip() 


# ------------- CLASSES FOR HTTP HANDLERS --------
class UserCreate(UserBase):
    password : str = Field(min_length = 8, max_length = 64)

class UserLogin(BaseModel):
    email : EmailStr
    password : str



class UserResponse(UserBase):

    id : PyObjectId = Field(alias = "_id", default_factory = PyObjectId)

    is_active:   bool = True
    is_verified: bool = False

    created_at : datetime = Field(default_factory = datetime.now)
    updated_at : datetime = Field(default_factory = datetime.now) 

    model_config = ConfigDict(populate_by_name=True,
                              arbitrary_types_allowed=True)


# --------------- CLASSES FOR MONGODB -------------
class UserInDB(UserResponse):
    hashed_password : str 