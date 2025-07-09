import asyncio
from models.database import users_collection

async def check_users():
    try:
        users = await users_collection.find().to_list(length=None)
        print(f"Total users in database: {len(users)}")
        for user in users:
            print(f"User: {user.get('email')} - {user.get('username')}")
            print(f"Password hash exists: {bool(user.get('hashed_password'))}")
            print(f"User ID: {user.get('_id')}")
            print("---")
    except Exception as e:
        print(f"Error checking users: {e}")

if __name__ == "__main__":
    asyncio.run(check_users())
