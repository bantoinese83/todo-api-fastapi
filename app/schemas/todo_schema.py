from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional, List


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    estimated_time: Optional[float] = None
    actual_time: Optional[float] = None
    parent_id: Optional[uuid.UUID] = None
    priority_override: bool = False
    recurring: bool = False
    recurrence_interval: Optional[int] = None
    cost_estimate: Optional[float] = None
    actual_cost: Optional[float] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class Todo(TodoBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
