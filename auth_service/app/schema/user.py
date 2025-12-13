from pydantic import BaseModel, Field, EmailStr

from typing import Literal
from datetime import datetime
from bson import ObjectId

from schema.object_id import PyObjectId


# ------------- BASE CLASS FOR USER --------------
class UserBase(BaseModel):
    email : EmailStr
    name  : str

    role  : Literal["customer", "staff", "admin"] = "customer"


# ------------- CLASSES FOR HTTP HANDLERS --------
class UserCreate(UserBase):
    password : str = Field(min_length = 8, max_length = 64)

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(UserBase):

    id : PyObjectId = Field(alias = "_id", default_factory = PyObjectId)

    created_at : datetime = Field(default_factory = datetime.now)
    updated_at : datetime = Field(default_factory = datetime.now) 

    class Config:
        json_encoders = {
            ObjectId : str 
        }
        validate_by_name = True 
        arbitrary_types_allowed = True


# --------------- CLASSES FOR MONGODB -------------
class UserInDB(UserResponse):
    hashed_password : str 