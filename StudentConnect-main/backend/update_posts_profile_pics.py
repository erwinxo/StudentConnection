import asyncio
from models.database import posts_collection, users_collection

async def update_posts_with_profile_pictures():
    """Update existing posts to include author profile pictures"""
    try:
        print("Updating existing posts with profile pictures...")
        
        # Get all posts
        posts = await posts_collection.find().to_list(length=None)
        updated_count = 0
        
        for post in posts:
            author_username = post.get("author_username")
            if not author_username:
                continue
                
            # Get the user's current profile picture
            user = await users_collection.find_one({"username": author_username})
            if user:
                profile_picture = user.get("profile_picture", "")
                
                # Update the post with the profile picture
                result = await posts_collection.update_one(
                    {"_id": post["_id"]},
                    {"$set": {"author_profile_picture": profile_picture}}
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    print(f"✅ Updated post '{post.get('title', 'Untitled')}' by @{author_username}")
                    if profile_picture:
                        print(f"   Added profile picture: {profile_picture[:50]}...")
                    else:
                        print(f"   No profile picture for user @{author_username}")
        
        print(f"\n🎉 Successfully updated {updated_count} posts!")
        
    except Exception as e:
        print(f"❌ Error updating posts: {e}")

if __name__ == "__main__":
    asyncio.run(update_posts_with_profile_pictures())
