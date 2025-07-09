import asyncio
from models.database import get_user_by_email
from utils.auth import verify_password

async def test_login():
    try:
        # Test with existing user
        user = await get_user_by_email("test@example.com")
        if user:
            print(f"User found: {user['email']}")
            print(f"Username: {user['username']}")
            print(f"Has password hash: {bool(user.get('hashed_password'))}")
            
            # Test password verification
            test_passwords = ["testpassword", "password", "test123", "123456"]
            for pwd in test_passwords:
                is_valid = verify_password(pwd, user["hashed_password"])
                print(f"Password '{pwd}': {'✅ VALID' if is_valid else '❌ INVALID'}")
        else:
            print("User not found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_login())
