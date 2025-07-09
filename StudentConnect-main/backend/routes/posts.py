from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Query
from typing import List, Optional
from datetime import datetime
from models.schemas import PostCreate, PostResponse, PostType
from models.database import (
    create_post, 
    get_posts, 
    get_post_by_id,
    get_user_posts
)
from utils.auth import get_current_user
from utils.cloudinary import upload_file_to_cloudinary

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
async def create_new_post(
    title: str = Form(...),
    content: str = Form(...),
    post_type: PostType = Form(...),
    tags: Optional[str] = Form(""),
    job_link: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    document: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_user)
):
    # Parse tags
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
    
    post_data = {
        "title": title,
        "content": content,
        "post_type": post_type,
        "tags": tags_list,
        "author_id": str(current_user["_id"]),
        "author_name": current_user["name"],
        "author_username": current_user["username"],
        "author_profile_picture": current_user.get("profile_picture", ""),
        "comments_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Handle file upload for notes
    if post_type == PostType.notes and document:
        try:
            upload_result = await upload_file_to_cloudinary(
                document.file, 
                folder="documents"
            )
            post_data["document_url"] = upload_result["url"]
            post_data["document_name"] = document.filename
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload document: {str(e)}"
            )
    
    # Handle job post fields
    if post_type == PostType.jobs:
        if not job_link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job link is required for job posts"
            )
        post_data["job_link"] = job_link
        post_data["company"] = company
        post_data["location"] = location
    
    created_post = await create_post(post_data)
    
    return PostResponse(
        id=str(created_post["_id"]),
        title=created_post["title"],
        content=created_post["content"],
        post_type=created_post["post_type"],
        tags=created_post["tags"],
        author_id=created_post["author_id"],
        author_name=created_post["author_name"],
        author_username=created_post["author_username"],
        author_profile_picture=created_post.get("author_profile_picture", ""),
        document_url=created_post.get("document_url"),
        document_name=created_post.get("document_name"),
        job_link=created_post.get("job_link"),
        company=created_post.get("company"),
        location=created_post.get("location"),
        comments_count=created_post["comments_count"],
        created_at=created_post["created_at"],
        updated_at=created_post["updated_at"]
    )

@router.get("/", response_model=List[PostResponse])
async def get_all_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    post_type: Optional[PostType] = None,
    search: Optional[str] = None
):
    posts = await get_posts(skip=skip, limit=limit, post_type=post_type, search=search)
    
    return [
        PostResponse(
            id=str(post["_id"]),
            title=post["title"],
            content=post["content"],
            post_type=post["post_type"],
            tags=post["tags"],
            author_id=post["author_id"],
            author_name=post["author_name"],
            author_username=post["author_username"],
            author_profile_picture=post.get("author_profile_picture", ""),
            document_url=post.get("document_url"),
            document_name=post.get("document_name"),
            job_link=post.get("job_link"),
            company=post.get("company"),
            location=post.get("location"),
            comments_count=post["comments_count"],
            created_at=post["created_at"],
            updated_at=post["updated_at"]
        )
        for post in posts
    ]

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostResponse(
        id=str(post["_id"]),
        title=post["title"],
        content=post["content"],
        post_type=post["post_type"],
        tags=post["tags"],
        author_id=post["author_id"],
        author_name=post["author_name"],
        author_username=post["author_username"],
        author_profile_picture=post.get("author_profile_picture", ""),
        document_url=post.get("document_url"),
        document_name=post.get("document_name"),
        job_link=post.get("job_link"),
        company=post.get("company"),
        location=post.get("location"),
        comments_count=post["comments_count"],
        created_at=post["created_at"],
        updated_at=post["updated_at"]
    )

@router.get("/user/{username}", response_model=List[PostResponse])
async def get_user_posts_by_username(
    username: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    from models.database import get_user_by_username
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    posts = await get_user_posts(str(user["_id"]), skip=skip, limit=limit)
    
    return [
        PostResponse(
            id=str(post["_id"]),
            title=post["title"],
            content=post["content"],
            post_type=post["post_type"],
            tags=post["tags"],
            author_id=post["author_id"],
            author_name=post["author_name"],
            author_username=post["author_username"],
            author_profile_picture=post.get("author_profile_picture", ""),
            document_url=post.get("document_url"),
            document_name=post.get("document_name"),
            job_link=post.get("job_link"),
            company=post.get("company"),
            location=post.get("location"),
            comments_count=post["comments_count"],
            created_at=post["created_at"],
            updated_at=post["updated_at"]
        )
        for post in posts
    ]
