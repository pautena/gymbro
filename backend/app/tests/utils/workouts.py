from sqlmodel import Session

from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from app.workouts import repository as workout_repository
from app.workouts.models import Workout, WorkoutCreate


def create_random_workout(db: Session) -> Workout:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    name = random_lower_string()
    notes = random_lower_string()
    workout_in = WorkoutCreate(name=name, notes=notes)
    return workout_repository.create_workout(
        session=db, workout_in=workout_in, owner_id=owner_id
    )
