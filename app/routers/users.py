from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import UsersModel
from app.schemas.user import UserResponse
from app.services import user_service
from app.dependencies.permissions import RoleChecker

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UsersModel = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_users(search: str | None = None,
              is_active: bool | None = None,
              current_user: UsersModel = Depends(RoleChecker(["ADMIN"])),
              db: Session = Depends(get_db)
              ):
    return user_service.get_users(db,search, is_active)