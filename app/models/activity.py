from app.db.database import Base
from sqlalchemy import Column, Integer, VARCHAR, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class ClubActivitiesModel(Base):
    __tablename__ = "club_activities"
    id = Column(Integer, primary_key= True)
    club_id = Column(ForeignKey("clubs.id"), nullable= False)
    title = Column(VARCHAR(255), nullable= False)
    description = Column(Text, nullable=True)
    assignee_id = Column(ForeignKey("users.id"), nullable= True)
    status = Column(Enum("TODO","IN_PROGRESS","DONE"), nullable=False)
    priority = Column(Enum("LOW","MEDIUM","HIGH"), nullable=False)
    due_date = Column(DateTime, nullable= True)
    created_at = Column(DateTime, nullable= False, default=lambda: datetime.now(timezone.utc))

    club = relationship("ClubsModel",back_populates="activities")

    assignee = relationship("UsersModel",back_populates="assigned_activities")