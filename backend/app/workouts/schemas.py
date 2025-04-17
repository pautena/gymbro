import datetime
import uuid

from sqlmodel import Field, SQLModel

from app.workouts.models import WorkoutBase


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(WorkoutBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    date: datetime.date | None = Field(default=None)  # type: ignore


class WorkoutSchema(WorkoutBase):
    id: uuid.UUID


class WorkoutsSchema(SQLModel):
    data: list[WorkoutSchema]
    count: int
