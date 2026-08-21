from app.db.database import Base
from sqlalchemy import Column, Integer, VARCHAR, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class ClubsModel(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key= True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(ForeignKey("users.id"), nullable= False)
    created_at = Column(DateTime, nullable= False,  default=lambda: datetime.now(timezone.utc))

    owner = relationship("UsersModel",back_populates="owned_clubs")

    club_members = relationship("ClubMembersModel", back_populates="club")

    activities = relationship("ClubActivitiesModel",back_populates="club")


class ClubMembersModel(Base):
    __tablename__ = "club_members"
    club_id = Column(ForeignKey("clubs.id"), primary_key= True)
    user_id = Column(ForeignKey("users.id"), primary_key= True)
    role = Column(Enum("OWNER","MEMBER"), nullable= False)
    joined_at = Column(DateTime, nullable= False, default=lambda: datetime.now(timezone.utc))

    club = relationship("ClubsModel", back_populates="club_members")

    user = relationship("UsersModel",back_populates="club_memberships")