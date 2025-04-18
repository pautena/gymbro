import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.users.models import User


class WorkoutBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    notes: str | None = Field(default=None)
    date: datetime.date = Field(default_factory=datetime.date.today)


class Workout(WorkoutBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="workouts")
