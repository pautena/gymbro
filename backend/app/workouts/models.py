import uuid
from app.users.models import User
from sqlmodel import Field, Relationship, SQLModel

class WorkoutBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class WorkoutCreate(WorkoutBase):
    pass

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
