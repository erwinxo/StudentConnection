from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from models.schemas import CommentCreate, CommentResponse
from models.database import (
    create_comment,
    get_comments_by_post_id,
    get_post_by_id,
    posts_collection
)
from utils.auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
async def create_new_comment(
    comment: CommentCreate,
    current_user = Depends(get_current_user)
):
    # Check if post exists
    post = await get_post_by_id(comment.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    comment_data = {
        "content": comment.content,
        "post_id": comment.post_id,
        "parent_comment_id": comment.parent_comment_id,
        "author_id": str(current_user["_id"]),
        "author_name": current_user["name"],
        "author_username": current_user["username"],
        "author_profile_picture": current_user.get("profile_picture", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    created_comment = await create_comment(comment_data)
    
    # Update post comments count
    await posts_collection.update_one(
        {"_id": ObjectId(comment.post_id)},
        {"$inc": {"comments_count": 1}}
    )
    
    return CommentResponse(
        id=str(created_comment["_id"]),
        content=created_comment["content"],
        post_id=created_comment["post_id"],
        parent_comment_id=created_comment.get("parent_comment_id"),
        author_id=created_comment["author_id"],
        author_name=created_comment["author_name"],
        author_username=created_comment["author_username"],
        author_profile_picture=created_comment.get("author_profile_picture", ""),
        replies=[],
        created_at=created_comment["created_at"],
        updated_at=created_comment["updated_at"]
    )

@router.get("/{post_id}", response_model=List[CommentResponse])
async def get_post_comments(post_id: str):
    # Check if post exists
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    comments = await get_comments_by_post_id(post_id)
    
    # Organize comments with replies
    comments_dict = {}
    root_comments = []
    
    for comment in comments:
        comment_response = CommentResponse(
            id=str(comment["_id"]),
            content=comment["content"],
            post_id=comment["post_id"],
            parent_comment_id=comment.get("parent_comment_id"),
            author_id=comment["author_id"],
            author_name=comment["author_name"],
            author_username=comment["author_username"],
            author_profile_picture=comment.get("author_profile_picture", ""),
            replies=[],
            created_at=comment["created_at"],
            updated_at=comment["updated_at"]
        )
        
        comments_dict[str(comment["_id"])] = comment_response
        
        if not comment.get("parent_comment_id"):
            root_comments.append(comment_response)
    
    # Attach replies to parent comments
    for comment in comments:
        if comment.get("parent_comment_id"):
            parent_id = comment["parent_comment_id"]
            if parent_id in comments_dict:
                comments_dict[parent_id].replies.append(comments_dict[str(comment["_id"])])
    
    return root_comments
