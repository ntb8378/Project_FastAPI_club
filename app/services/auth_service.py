from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import UsersModel
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password

from app.core import exception

def register_user(db: Session, user: UserCreate):
    # Kiểm tra email đã tồn tại
    existing_user = db.query(UsersModel).filter(UsersModel.email == user.email).first()
    if existing_user:
        exception.bad_request("Email đã được sử dụng")
    # Hash password
    password_hash = hash_password(user.password)
    # Tạo user mới
    new_user = UsersModel(
        email=user.email,
        password_hash=password_hash,
        full_name=user.full_name
    )
    # Lưu database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# xác thực tài khoản và đăng nhập
def authenticate_user(db: Session, user_data:UserLogin):
    user = db.query(UsersModel).filter(UsersModel.email == user_data.email).first()
    # Kiểm tra user có tồn tại không VÀ mật khẩu có khớp không
    if not user or not verify_password(user_data.password, user.password_hash):
        exception.unauthorized("Email hoặc mật khẩu không chính xác")

    if not user.is_active:
        exception.unauthorized("Tài khoản này đã bị tạm khóa")
    
    return user