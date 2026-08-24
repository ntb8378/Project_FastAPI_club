from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

# file này dùng để dùng chung cho nhiều schemas User
# br cái này
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str = Field(
        min_length=6,
        max_length=100
    )

# tạo thêm để dùng cho login
class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)