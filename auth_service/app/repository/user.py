from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional
from pymongo import ReturnDocument

from app.db.client import get_user_collection

from app.schema.user import UserInDB, UserUpdate
from app.schema.object_id import PyObjectId

from app.core.password import verify_password, hash_password


class UserRepository:

    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_user_collection()
    
    async def insert(self, user: UserInDB) -> UserInDB:
        user_dict = user.model_dump(by_alias = True, exclude_none = True)
        result = await self.collection.insert_one(user_dict) 
        user.id = result.inserted_id
        return user

    async def update(self, id : PyObjectId, update : UserUpdate) -> UserInDB:
        update_dict = update.model_dump(by_alias = True, exclude_none = True)
        result = await self.collection.find_one_and_update({"_id": id}, {"$set": update_dict}, return_document = ReturnDocument.AFTER)
        if result:
            return UserInDB(**result)
        return None

    async def update_password(self, email : str, old_password : str, new_password : str) -> None:
        result = await self.collection.find_one({"email": email})
        if result is None:
            return
        if verify_password(old_password, result["hashed_password"]) == False:
            return
        result["hashed_password"] = hash_password(new_password)
        await self.collection.find_one_and_update({"email": email}, {"$set": result})

    async def find(self, email : str = None, id: PyObjectId = None) -> Optional[UserInDB]:
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
