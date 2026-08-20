from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ClubBase(BaseModel):
    name : str 
    description : str | None = None

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    name : str | None = None
    description : str | None = None

class ClubResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClubMemberBase(BaseModel):
    user_id: int

class ClubMemberCreate(ClubMemberBase):
    pass

class ClubMemberUpdate(BaseModel):
    role: str | None = None

class ClubMemberResponse(BaseModel):
    club_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)