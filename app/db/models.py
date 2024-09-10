import enum
import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    func,
    Enum,
    Float,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PriorityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.MEDIUM, nullable=False)
    due_date = Column(DateTime, nullable=True)
    tags = Column(JSONB, nullable=True)
    assigned_to = Column(String(100), nullable=True)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    estimated_time = Column(Float, nullable=True)
    actual_time = Column(Float, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("todos.id"), nullable=True)
    priority_override = Column(Boolean, default=False, nullable=False)
    recurring = Column(Boolean, default=False, nullable=False)
    recurrence_interval = Column(Integer, nullable=True)
    cost_estimate = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="todos")
    subtasks = relationship("Todo", backref="parent", remote_side=[id])

    __table_args__ = (
        CheckConstraint("char_length(title) > 0", name="check_title_length"),
        UniqueConstraint("title", "assigned_to", name="uix_title_assigned_to"),
        Index("ix_todos_status_priority", "status", "priority"),
    )
