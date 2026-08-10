from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    """
    return await AuthService.register(db, user_in=user_in)

@router.post("/login", response_model=Token)
async def login_access_token(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    return await AuthService.authenticate(db, user_in=user_in)

@router.post("/token", response_model=Token)
async def login_access_token_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2-compatible login for Swagger UI.
    """
    user_in = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return await AuthService.authenticate(db, user_in=user_in)