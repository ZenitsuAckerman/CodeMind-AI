from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin, UserRead
from app.schemas.token import Token
from app.repositories.user_repository import user_repository
from app.utils.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_in: UserCreate) -> UserRead:
        user = await user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )
        user = await user_repository.create(db, obj_in=user_in)
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, user_in: UserLogin) -> Token:
        user = await user_repository.get_by_email(db, email=user_in.email)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not verify_password(user_in.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
            
        access_token = create_access_token(subject=str(user.id))
        return Token(access_token=access_token, token_type="bearer")
