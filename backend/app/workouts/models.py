import datetime
from typing import Optional
import uuid
from app.users.models import User
from sqlmodel import Field, Relationship, SQLModel

class WorkoutBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    notes: Optional[str] = Field()
    date: datetime.date = Field(default_factory=datetime.date.today)

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(WorkoutBase):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    date: Optional[datetime.date] = Field(default=None)


class Workout(WorkoutBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="workouts")


class WorkoutPublic(WorkoutBase):
    id: uuid.UUID

class WorkoutsPublic(SQLModel):
    data: list[WorkoutPublic]
    count: int
