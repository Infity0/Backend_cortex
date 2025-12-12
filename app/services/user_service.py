import os
import aiofiles
from typing import Optional
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.core.config import settings


class UserService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def update_profile(self, user_id: int, username: Optional[str] = None):
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if username is not None:
            user.username = username
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def upload_avatar(self, user_id: int, file: UploadFile):
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'

        upload_dir = os.path.join(settings.UPLOAD_DIR, 'avatars')
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"avatar_{user_id}.{ext}"
        filepath = os.path.join(upload_dir, filename)
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            user.avatar_url = f"/uploads/avatars/{filename}"
            await self.db.commit()
        
        return {"message": "Avatar uploaded successfully", "avatar_url": user.avatar_url}
    
    async def change_password(self, user_id: int, old_password: str, new_password: str):
        """Change user password"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

        user.password_hash = get_password_hash(new_password)
        await self.db.commit()
        
        return {"message": "Password changed successfully"}
    
    async def delete_account(self, user_id: int):
        """Delete user account"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = False
        await self.db.commit()
        
        return {"message": "Account deleted successfully"}
