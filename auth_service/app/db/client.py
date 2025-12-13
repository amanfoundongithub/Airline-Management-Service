from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from config.settings import settings

# Global variables to hold the database client and the database object
client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


# ---------- MONGO CONNECTION FUNCTIONS -----------
async def connect_with_mongo():
    global client, database

    try: 
        client = AsyncIOMotorClient(
            settings.mongo.uri, 
            serverSelectionTimeoutMS = 5000,
            uuidRepresentation = "standard"
        )
        await client.admin.command("ping")

        print("[INFO]\tSuccessfully connected to MongoDB.")
        database = client[settings.mongo.db_name]
        print(f"[INFO]\tUsing the database: {settings.mongo.db_name}")

    except Exception as e:
        print(f"[ERROR] Unable to connect to MongoDB: {e}")
        raise 

async def disconnect_with_mongo():
    global client 

    if client:
        client.close()
        print(f"[INFO] Closing connection with {settings.mongo.db_name}")


async def get_user_collection() -> AsyncIOMotorCollection:
    if database is None:
        raise ConnectionError(f"[ERROR] Connect to MongoDB before getting collection.")
    return database[settings.mongo.user_collection_name]
