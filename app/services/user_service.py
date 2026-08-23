from sqlalchemy.orm import Session

from app.models.user import UsersModel


def get_users(db: Session,search: str | None = None,is_active: bool | None = None):
    query = db.query(UsersModel)
    if search:
        query = query.filter((UsersModel.full_name.ilike(f"%{search}%")) |(UsersModel.email.ilike(f"%{search}%")))
    if is_active is not None:
        query = query.filter(UsersModel.is_active == is_active)
    return query.all()