import asyncio
from models.database import get_user_by_email
from utils.auth import verify_password

async def test_common_passwords():
    """Test common passwords against existing users"""
    
    # Common test passwords to try
    common_passwords = [
        "password", "password123", "123456", "admin", "test", 
        "user123", "qwerty", "abc123", "testpass", "demo123"
    ]
    
    # Get all users
    users = [
        "jeswanth1811@gmail.com",
        "test@example.com", 
        "jaswantsai1118@gmail.com",
        "newuser@example.com",
        "freshuser@example.com"
    ]
    
    print("Testing common passwords against user accounts...\n")
    
    for email in users:
        user = await get_user_by_email(email)
        if user:
            print(f"🔍 Testing passwords for: {email} ({user['username']})")
            found_password = False
            
            for password in common_passwords:
                is_valid = verify_password(password, user["hashed_password"])
                if is_valid:
                    print(f"  ✅ PASSWORD FOUND: '{password}'")
                    found_password = True
                    break
            
            if not found_password:
                print(f"  ❌ No common password found")
            print()

if __name__ == "__main__":
    asyncio.run(test_common_passwords())
