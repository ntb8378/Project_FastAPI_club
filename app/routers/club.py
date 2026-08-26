from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import UsersModel
from app.schemas.club import ClubCreate, ClubResponse, ClubUpdate, ClubMemberCreate, ClubMemberResponse
from app.services import club_service


router = APIRouter(
    prefix="/clubs",
    tags=["Clubs"]
)

# tạo club đồng thời thêm người tạo thành owner
@router.post("/",response_model=ClubResponse,status_code=status.HTTP_201_CREATED)
def create_club(club: ClubCreate,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.create_club(db,club,current_user.id)

# search và trả về khi bạn là member hoặc owner của club đó
@router.get("/", response_model=list[ClubResponse])
def get_clubs(search: str | None = None,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.get_clubs(db,current_user.id,search)

# chỉ thành viên và owner của club mới được xem 
@router.get("/{club_id}", response_model=ClubResponse)
def get_club_detail(club_id: int,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.get_club_detail(db,club_id,current_user.id)

# cập nhật phần muốn sửa chứ k cập nhật hết
@router.patch("/{club_id}", response_model=ClubResponse)
def update_club(club_id: int,club_data: ClubUpdate,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.update_club(db,club_id,club_data,current_user.id)


@router.delete("/{club_id}", status_code=status.HTTP_200_OK)
def delete_club(club_id: int,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.delete_club(db,club_id,current_user.id)


 
# chỉ owner mới thêm được thành viên cho club_member
@router.post("/{club_id}/members", status_code=201)
def add_member(club_id: int,member: ClubMemberCreate,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.add_member(db,club_id,member.user_id,current_user.id)


@router.delete("/{club_id}/members/{user_id}", status_code=204)
def remove_member(club_id: int,user_id: int,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.remove_member(db,club_id,user_id,current_user.id)

# trả về danh sách thành viên clb , 
@router.get("/{club_id}/members",response_model=list[ClubMemberResponse])
def get_members(club_id: int,current_user: UsersModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return club_service.get_members(db,club_id,current_user.id)