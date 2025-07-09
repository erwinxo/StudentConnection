from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from models.schemas import UserCreate, UserLogin, UserResponse, Token, UserUpdate, ForgotPasswordRequest, ResetPasswordRequest
from models.database import (
    get_user_by_email, 
    get_user_by_username, 
    create_user, 
    update_user,
    get_user_by_id,
    users_collection,
    posts_collection
)
from utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from utils.email import (
    generate_reset_token,
    store_reset_token,
    validate_reset_token,
    clear_reset_token,
    send_reset_email
)
from utils.cloudinary import upload_file_to_cloudinary, delete_file_from_cloudinary

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    # Check if user already exists
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_username = await get_user_by_username(user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "username": user.username,
        "name": user.name,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    created_user = await create_user(user_data)
    return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        username=created_user["username"],
        name=created_user["name"],
        bio=created_user["bio"],
        profile_picture=created_user["profile_picture"],
        created_at=created_user["created_at"]
    )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        username=current_user["username"],
        name=current_user["name"],
        bio=current_user["bio"],
        profile_picture=current_user["profile_picture"],
        created_at=current_user["created_at"]
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user = Depends(get_current_user)
):
    # Check if username is being updated and if it's available
    if user_update.username and user_update.username != current_user["username"]:
        existing_username = await get_user_by_username(user_update.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    updated_user = await update_user(str(current_user["_id"]), update_data)
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        name=updated_user["name"],
        bio=updated_user["bio"],
        profile_picture=updated_user["profile_picture"],
        created_at=updated_user["created_at"]
    )

@router.get("/user/{username}", response_model=UserResponse)
async def get_user_profile(username: str):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        username=user["username"],
        name=user["name"],
        bio=user["bio"],
        profile_picture=user["profile_picture"],
        created_at=user["created_at"]
    )

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Send password reset email with secure token using Web3Forms
    """
    user = await get_user_by_email(request.email)
    if not user:
        return {"message": "If the email exists, a password reset link has been sent"}
    try:
        reset_token = generate_reset_token()
        token_stored = await store_reset_token(request.email, reset_token)
        if not token_stored:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process password reset request"
            )
        email_sent = send_reset_email(request.email, reset_token)
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send password reset email"
            )
        return {"message": "If the email exists, a password reset link has been sent"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in forgot password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process password reset request"
        )

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """
    Reset password using valid token
    """
    # Validate the reset token
    user = await validate_reset_token(request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    try:
        # Hash the new password
        hashed_password = get_password_hash(request.new_password)
        
        # Update user's password
        result = await users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "hashed_password": hashed_password,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        # Clear the reset token
        await clear_reset_token(user["email"])
        
        return {"message": "Password has been reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in reset password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )

@router.post("/profile/picture", response_model=UserResponse)
async def update_profile_picture(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Update user profile picture"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Validate file size (max 5MB)
    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB"
        )
    
    try:
        # Delete old profile picture if it exists
        if current_user.get("profile_picture"):
            old_url = current_user["profile_picture"]
            # Extract public_id from Cloudinary URL
            if "cloudinary.com" in old_url:
                # Extract public_id from URL (this is a simplified extraction)
                public_id = old_url.split("/")[-1].split(".")[0]
                try:
                    await delete_file_from_cloudinary(f"profile_pictures/{public_id}")
                except:
                    pass  # Ignore errors when deleting old image
        
        # Upload new profile picture
        upload_result = await upload_file_to_cloudinary(
            file_content, 
            folder="profile_pictures"
        )
        
        # Update user in database
        update_data = {
            "profile_picture": upload_result["url"],
            "updated_at": datetime.utcnow()
        }
        
        updated_user = await update_user(str(current_user["_id"]), update_data)
        
        # Update all existing posts by this user with the new profile picture
        try:
            await posts_collection.update_many(
                {"author_username": current_user["username"]},
                {"$set": {"author_profile_picture": upload_result["url"]}}
            )
            print(f"✅ Updated profile picture in all posts for user @{current_user['username']}")
        except Exception as e:
            print(f"⚠️ Warning: Could not update posts with new profile picture: {e}")
            # Don't fail the request if post updates fail
        
        return UserResponse(
            id=str(updated_user["_id"]),
            email=updated_user["email"],
            username=updated_user["username"],
            name=updated_user["name"],
            bio=updated_user["bio"],
            profile_picture=updated_user["profile_picture"],
            created_at=updated_user["created_at"]
        )
        
    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload profile picture"
        )
