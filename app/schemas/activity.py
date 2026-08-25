from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class ActivityStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class ActivityPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ActivityCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: ActivityPriority = ActivityPriority.MEDIUM
    assignee_id: int | None = None


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ActivityStatus | None = None
    priority: ActivityPriority | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None


class ActivityResponse(BaseModel):
    title: str
    description: str | None = None
    status: ActivityStatus
    priority: ActivityPriority
    due_date: datetime | None = None
    id: int
    club_id: int
    assignee_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)