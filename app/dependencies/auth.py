from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from app.core.config import settings
from app.core import exception
from app.db.database import get_db
from app.models.user import UsersModel


# Sử dụng HTTPBearer để lấy token từ header
reusable_oauth2 = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    db: Session = Depends(get_db)
):
    # Tự động lấy chuỗi Token nguyên bản
    token = credentials.credentials

    try:
        # Bước 1: Giải mã Token bằng khóa bí mật
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        # Trong hệ thống hiện tại, "sub" lưu email
        email: str = payload.get("sub")

        if email is None:
            exception.unauthorized("Không thể xác thực thông tin đăng nhập")

    except jwt.ExpiredSignatureError:
        exception.unauthorized("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại")

    except jwt.PyJWTError:
        exception.unauthorized("Không thể xác thực thông tin đăng nhập")
    # Bước 2: Truy vấn thông tin người dùng từ DB thông qua SQLAlchemy ORM
    user = db.query(UsersModel).filter(UsersModel.email == email).first()

    if user is None:
        exception.not_found("Người dùng không tồn tại trên hệ thống")
    # Bước 3: Kiểm tra xem tài khoản có đang bị khóa hay không
    if not user.is_active:
        exception.unauthorized("Tài khoản này đã bị tạm khóa!")
    # Trả về đối tượng người dùng hoàn chỉnh cho endpoint kế tiếp
    return user