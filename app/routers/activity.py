from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate, ActivityStatus, ActivityPriority
from app.services.activity_service import create_activity,get_club_activities, get_activity, update_activity, delete_activity
from app.dependencies.auth import get_current_user
from fastapi import Query


router = APIRouter(
    tags=["Activities"]
)


#  thêm hoạt động cho club , chỉ thành viên mới có quyền
@router.post("/clubs/{club_id}/activities",response_model=ActivityResponse)
def create_club_activity(club_id: int,activity_data: ActivityCreate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return create_activity(db,club_id,activity_data,current_user.id)

# lấy danh sách hoạt động của clb mà mình là thành viên
@router.get(
    "/clubs/{club_id}/activities",
    response_model=list[ActivityResponse]
)
def get_club_activitie(
    club_id: int,
    status: ActivityStatus | None = None,
    priority: ActivityPriority | None = None,
    assignee_id: int | None = None,
    title: str | None = None,

    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    # chỉ cho phép sort_by nhận created_at hoặc due_date
    sort_by: str | None = Query(
        None,
        pattern="^(created_at|due_date)$"
    ),

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_club_activities(
        db=db,
        club_id=club_id,
        current_user_id=current_user.id,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        title=title,
        limit=limit,
        offset=offset,
        sort_by=sort_by
    )

# hiển thị ra hoạt động dựa trên id của hoạt động
@router.get("/activities/{activity_id}",response_model=ActivityResponse)
def get_activity_detail(activity_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return get_activity(db,activity_id,current_user.id)

# cập nhật những trường muốn đổi cho hoạt động
@router.patch("/activities/{activity_id}",response_model=ActivityResponse
)
def update_activity_detail(activity_id: int,activity_data: ActivityUpdate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return update_activity(db,activity_id,activity_data,current_user.id)


# chỉ thành viên thuộc đúng quyền mới có thể xóa hoạt động
@router.delete("/activities/{activity_id}",status_code=204)
def delete_activity_detail(activity_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return delete_activity(db,activity_id,current_user.id)