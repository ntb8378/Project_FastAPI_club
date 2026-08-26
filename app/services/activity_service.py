from sqlalchemy.orm import Session

from app.models.activity import ClubActivitiesModel
from app.models.club import ClubsModel, ClubMembersModel
from app.models.user import UsersModel
from app.core import exception
from app.schemas.activity import ActivityCreate, ActivityStatus, ActivityPriority, ActivityUpdate


# thêm hoạt động cho club , chỉ thành viên của câu lạc bộ mới có thể thêm hoạt động
def create_activity(db: Session,club_id: int,activity_data: ActivityCreate,current_user_id: int):
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    if activity_data.assignee_id is not None:

        assignee_member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == activity_data.assignee_id).first())

        if not assignee_member:
            exception.bad_request(
                "Người được giao phải là thành viên của câu lạc bộ"
            )

    new_activity = ClubActivitiesModel(
        club_id=club_id,
        title=activity_data.title,
        description=activity_data.description,
        due_date=activity_data.due_date,
        # .value vì priority đang là enum , . tới để lấy ra được nội dung bên trong
        priority=activity_data.priority.value,
        status="TODO",
        assignee_id=activity_data.assignee_id
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return new_activity


# chỉ xem được clb mà mình tham gia , tìm hoạt động dựa trên club id đó 
def get_club_activities(db: Session,club_id: int,current_user_id: int,
status: ActivityStatus | None = None, priority: ActivityPriority | None = None, assignee_id: int | None = None, title: str | None = None,
# ofset bỏ qua phần tử đầu , tính từ trang tiếp theo , vd limit = 5 ofset = 5 thì nó sẽ hiện trang 2 gồm phàn tử từ 6 đến 11
limit: int = 10,offset: int = 0,sort_by: str | None = None):
    club = (db.query(ClubsModel).filter(ClubsModel.id == club_id).first())

    if not club:
        exception.not_found(
            "Không tìm thấy câu lạc bộ"
        )

    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    query = (db.query(ClubActivitiesModel).filter(ClubActivitiesModel.club_id == club_id))


    if status is not None:
        query = query.filter(ClubActivitiesModel.status == status.value)
    if priority is not None:
        query = query.filter(ClubActivitiesModel.priority == priority.value)
    if assignee_id is not None:
        query = query.filter(ClubActivitiesModel.assignee_id == assignee_id)
    if title is not None:
        query = query.filter(ClubActivitiesModel.title.ilike(f"%{title}%"))
    # Sort
    if sort_by == "created_at":
        query = query.order_by(
            ClubActivitiesModel.created_at
        )

    elif sort_by == "due_date":
        query = query.order_by(
            ClubActivitiesModel.due_date
        )

    # Pagination
    query = query.offset(offset).limit(limit)

    return query.all()



# tìm hoạt động dựa trên id của hoạt động , chỉ thành viên của club chứa hoạt động đó mới coi được
def get_activity(db: Session,activity_id: int,current_user_id: int):
    activity = (db.query(ClubActivitiesModel).filter(ClubActivitiesModel.id == activity_id).first())

    if not activity:
        exception.not_found(
            "Không tìm thấy hoạt động"
        )

    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == activity.club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    return activity


#  chỉ thành viên clb mới có thể cập nhật hoạt động
def update_activity(db: Session,activity_id: int,activity_data: ActivityUpdate,current_user_id: int):
    activity = (db.query(ClubActivitiesModel).filter(ClubActivitiesModel.id == activity_id).first())

    if not activity:
        exception.not_found(
            "Không tìm thấy hoạt động"
        )

    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == activity.club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    update_data = activity_data.model_dump(exclude_unset=True)

    # Kiểm tra người được giao
    if "assignee_id" in update_data:
        assignee_id = update_data["assignee_id"]

        if assignee_id is not None:
            assignee_member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == activity.club_id,ClubMembersModel.user_id == assignee_id).first())

            if not assignee_member:
                exception.bad_request(
                    "Người được giao phải là thành viên của câu lạc bộ"
                )

    for field, value in update_data.items():

        if field in ["status", "priority"]:
            value = value.value

        # activity.title = "Tên mới"
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)

    return activity


#  chỉ thành viên mới có quyền xóa hoạt động của club mà mình tham gia
def delete_activity(db: Session,activity_id: int,current_user_id: int):
    activity = (db.query(ClubActivitiesModel).filter(ClubActivitiesModel.id == activity_id).first())

    if not activity:
        exception.not_found(
            "Không tìm thấy hoạt động"
        )

    member = (db.query(ClubMembersModel).filter(ClubMembersModel.club_id == activity.club_id,ClubMembersModel.user_id == current_user_id).first())

    if not member:
        exception.forbidden(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    if member.role != "OWNER":
        exception.forbidden(
            "Bạn không có quyền xóa hoạt động"
        )

    db.delete(activity)
    db.commit()

    return None