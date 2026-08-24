from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ClubBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255
    )
    description: str | None = None

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class ClubMemberCreate(BaseModel):
    user_id: int

class ClubMemberUpdate(BaseModel):
    role: str | None = None

class ClubMemberResponse(BaseModel):
    club_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)