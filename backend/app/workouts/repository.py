import uuid

from sqlmodel import Session

from app.workouts.models import Workout, WorkoutCreate


def create_workout(
    *, session: Session, workout_in: WorkoutCreate, owner_id: uuid.UUID
) -> Workout:
    db_workout = Workout.model_validate(workout_in, update={"owner_id": owner_id})
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    return db_workout
