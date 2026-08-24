from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services import auth_service
from app.core.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)\
# tìm hiểu tại sao có db: Session = Depends(get_db)
def register(user: UserCreate,db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):
    authenticated_user = auth_service.authenticate_user(db, user)
    if authenticated_user:
    # Tạo JWT Access Token, nhét role_name vào payload để dùng cho Authorization
        access_token = create_access_token(data={"sub": user.email})
        return {
            "message": "Đăng nhập thành công",
            "access_token": access_token,
            "token_type": "bearer",
            "data": {
                "sub": user.email,
            }
        }
