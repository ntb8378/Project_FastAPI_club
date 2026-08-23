from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    title: str
    description: str | None = None
    status: str
    priority: str
    due_date: datetime | None = None

class ActivityCreate(ActivityBase):
    assignee_id: int | None = None

class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str
    priority: str
    due_date: datetime | None = None
    assignee_id: int | None = None

class ActivityResponse(ActivityBase):
    id: int
    club_id: int
    assignee_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)