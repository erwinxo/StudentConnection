import asyncio
from models.database import posts_collection

async def check_posts():
    try:
        posts = await posts_collection.find().limit(3).to_list(length=None)
        print(f"Total posts found: {len(posts)}")
        for post in posts:
            print(f"Post: {post.get('title', 'No title')}")
            print(f"Author: {post.get('author_name', 'Unknown')} (@{post.get('author_username', 'unknown')})")
            print(f"Profile picture: {post.get('author_profile_picture', 'None')}")
            print("---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_posts())
