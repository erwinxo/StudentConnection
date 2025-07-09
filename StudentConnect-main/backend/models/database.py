from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "haripriya_db")

print("=== DATABASE CONFIGURATION ===")
print(f"MongoDB URL: {MONGODB_URL}")
print(f"Database Name: {DATABASE_NAME}")
print("=== END DATABASE CONFIGURATION ===")

try:
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    print("✅ Database connection initialized successfully")
except Exception as e:
    print(f"❌ Database connection error: {e}")

# Collections
users_collection = database.get_collection("users")
posts_collection = database.get_collection("posts")
comments_collection = database.get_collection("comments")

async def test_database_connection():
    """Test database connection"""
    try:
        # Test connection by pinging the database
        await database.command('ping')
        print("✅ Database connection test successful")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def create_object_id():
    return str(ObjectId())

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def get_user_by_id(user_id: str):
    return await users_collection.find_one({"_id": ObjectId(user_id)})

async def get_user_by_username(username: str):
    return await users_collection.find_one({"username": username})

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return await users_collection.find_one({"_id": result.inserted_id})

async def update_user(user_id: str, update_data: dict):
    await users_collection.update_one(
        {"_id": ObjectId(user_id)}, 
        {"$set": update_data}
    )
    return await get_user_by_id(user_id)

async def create_post(post_data: dict):
    result = await posts_collection.insert_one(post_data)
    return await posts_collection.find_one({"_id": result.inserted_id})

async def get_posts(skip: int = 0, limit: int = 20, post_type: Optional[str] = None, search: Optional[str] = None):
    query = {}
    
    if post_type:
        query["post_type"] = post_type
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}},
            {"author_name": {"$regex": search, "$options": "i"}},
            {"author_username": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = posts_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def get_post_by_id(post_id: str):
    return await posts_collection.find_one({"_id": ObjectId(post_id)})

async def create_comment(comment_data: dict):
    result = await comments_collection.insert_one(comment_data)
    return await comments_collection.find_one({"_id": result.inserted_id})

async def get_comments_by_post_id(post_id: str):
    cursor = comments_collection.find({"post_id": post_id}).sort("created_at", 1)
    return await cursor.to_list(length=None)

async def get_user_posts(user_id: str, skip: int = 0, limit: int = 20):
    cursor = posts_collection.find({"author_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
