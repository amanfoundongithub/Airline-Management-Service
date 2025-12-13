from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional

from db.client import get_user_collection

from schema.user import UserInDB
from schema.object_id import PyObjectId


class UserRepository:

    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_user_collection()
    
    async def insert(self, user: UserInDB) -> UserInDB:
        user_dict = user.model_dump(by_alias = True, exclude_none = True)
        result = await self.collection.insert_one(user_dict) 
        user.id = result.inserted_id

        return user 

    async def find(self, email : str = None,id: PyObjectId = None) -> Optional[UserInDB]:
        query = {}
        if email:
            query["email"] = email 
        elif id:
            query["_id"] = id 
        else:
            raise ValueError("At least one of the email or Id must be provided")
        
        user_dict = await self.collection.find_one(query)
        if user_dict:
            return UserInDB(**user_dict)
        else: 
            return None 
    

def get_user_repository() -> UserRepository:
    return UserRepository() 
