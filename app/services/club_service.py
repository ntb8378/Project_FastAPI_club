from sqlalchemy.orm import Session
from app.models.club import ClubsModel, ClubMembersModel
from app.models.user import UsersModel
from app.schemas.club import ClubCreate, ClubUpdate
from app.core import exception

def create_club(db: Session,club: ClubCreate,current_user_id: int):
    if not club.name.strip():
        exception.bad_request("Tên club không được để trống")
    
    new_club = ClubsModel(
        name=club.name.strip(),
        description=club.description,
        owner_id=current_user_id
    )

    db.add(new_club)

    # Lấy ID của club sau khi INSERT
    db.flush()

    owner_member = ClubMembersModel(
        club_id=new_club.id,
        user_id=current_user_id,
        role="OWNER"
    )

    db.add(owner_member)

    db.commit()
    db.refresh(new_club)

    return new_club


# trả về những club mà bạn tham gia (member, owner)
def get_clubs(db: Session,current_user_id: int,search: str | None = None):
    # club member có chứa club_id và user_id
    # ghim thêm bảng clubmembermodel để so sánh 
    query = (db.query(ClubsModel).join(ClubMembersModel,ClubsModel.id == ClubMembersModel.club_id).filter(ClubMembersModel.user_id == current_user_id))

    if search:
        query = query.filter(ClubsModel.name.ilike(f"%{search}%"))

    return query.all()


# chỉ thành viên câu lạc bộ mới được xem
def get_club_detail(db: Session,club_id: int,current_user_id: int):
    # Kiểm tra club tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    # Kiểm tra user có phải thành viên không
    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == current_user_id).first())
    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ này"
        )
    return club


# chỉ owner mới được quyền sửa
def update_club(db: Session,club_id: int,club_data: ClubUpdate,current_user_id: int):
    # Kiểm tra club tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found("Không tìm thấy câu lạc bộ")

    # Kiểm tra OWNER
    if club.owner_id != current_user_id:
        exception.forbidden("Chỉ OWNER mới có quyền cập nhật câu lạc bộ")

    if club_data.name is not None and not club_data.name.strip():
        exception.bad_request("Tên club không được để trống")

    # exclude_unset=True bỏ qua field nào không được gửi lên
    update_data = club_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(club, key, value)

    db.commit()
    db.refresh(club)

    return club


def delete_club(db: Session,club_id: int,current_user_id: int):
    # Kiểm tra club tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    # Kiểm tra OWNER
    if club.owner_id != current_user_id:
        exception.forbidden(
            "Chỉ OWNER mới có quyền xóa câu lạc bộ"
        )

    # Lấy tất cả member của club
    members = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id).all())

    # Xóa từng member
    for member in members:
        db.delete(member)

    # Xóa club
    db.delete(club)
    db.commit()




#  thêm thành viên cho club_member
def add_member(db: Session,club_id: int,user_id: int,current_user_id: int):
    # Kiểm tra club tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )
    # Kiểm tra OWNER
    if club.owner_id != current_user_id:
        exception.forbidden(
            "Chỉ OWNER mới có quyền thêm thành viên"
        )
    # Kiểm tra user tồn tại
    user = (db.query(UsersModel).filter(UsersModel.id == user_id).first())

    if not user:
        exception.not_found(
            "Không tìm thấy người dùng"
        )

    # Kiểm tra thành viên đã tồn tại
    existing_member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == user_id).first())

    if existing_member:
        exception.conflict(
            "Người dùng đã là thành viên của câu lạc bộ"
        )
    # Thêm member mới
    new_member = ClubMembersModel(
        club_id=club_id,
        user_id=user_id,
        role="MEMBER"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# xóa thành viên khỏi club_member
def remove_member(db: Session,club_id: int,user_id: int,current_user_id: int):
    # Kiểm tra club tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    # Kiểm tra người thực hiện có phải OWNER không
    if club.owner_id != current_user_id:
        exception.forbidden(
            "Chỉ OWNER mới có quyền xóa thành viên"
        )

    # Tìm thành viên cần xóa
    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == user_id).first())

    if not member:
        exception.not_found(
            "Người dùng không phải thành viên của câu lạc bộ"
        )

    # Không cho xóa OWNER
    if member.user_id == club.owner_id:
        exception.forbidden(
            "Không thể xóa OWNER của câu lạc bộ"
        )

    # Xóa member
    db.delete(member)
    db.commit()



def get_members(db: Session,club_id: int,current_user_id: int):
    # Kiểm tra CLB tồn tại
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    # Kiểm tra người dùng có phải member của CLB không
    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    # Lấy danh sách member
    members = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id).all())
    return members