from fastapi import Depends
from app.dependencies.auth import get_current_user
from app.models.user import UsersModel
from app.core import exception


class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        # Lưu lại danh sách role được phép khi khởi tạo
        self.allowed_roles = allowed_roles

    def __call__(self,current_user: UsersModel = Depends(get_current_user)):
        # Kiểm tra role của user có nằm trong danh sách được phép không
        if current_user.role not in self.allowed_roles:
            exception.forbidden("Bạn không có quyền truy cập")

        return current_user