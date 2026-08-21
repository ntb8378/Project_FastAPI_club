from app.db.database import Base
from sqlalchemy import Column, Integer, VARCHAR, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class UsersModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True)
    email = Column(VARCHAR(255), unique=True , nullable= False)
    password_hash = Column(VARCHAR(255), nullable=False)
    full_name = Column(VARCHAR(255), nullable=False)
    role = Column(Enum("USER","ADMIN"), default= "USER", nullable= False)
    is_active = Column(Boolean, default= True, nullable= False)
    created_at = Column(DateTime, nullable= False,  default=lambda: datetime.now(timezone.utc))

    owned_clubs = relationship("ClubsModel",back_populates="owner")

    assigned_activities = relationship("ClubActivitiesModel",back_populates="assignee")

    club_memberships = relationship("ClubMembersModel",back_populates="user")