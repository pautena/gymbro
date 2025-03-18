from typing import Any
from app.users.dependencies import CurrentUser, SessionDep
from fastapi import APIRouter
from app.workouts.models import Workout, WorkoutCreate, WorkoutPublic, WorkoutsPublic
from sqlmodel import func, select

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.get("/", response_model=WorkoutsPublic)
def read_workouts(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve workouts.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Workout)
        count = session.exec(count_statement).one()
        statement = select(Workout).offset(skip).limit(limit)
        items = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Workout)
            .where(Workout.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Workout)
            .where(Workout.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        items = session.exec(statement).all()

    return WorkoutsPublic(data=items, count=count)


@router.post("/", response_model=WorkoutPublic)
def create_workout(
    *, session: SessionDep, current_user: CurrentUser, workout_in: WorkoutCreate
) -> Any:
    """
    Create new workout.
    """
    workout = Workout.model_validate(workout_in, update={"owner_id": current_user.id})
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout