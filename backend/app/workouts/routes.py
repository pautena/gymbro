from typing import Any
import uuid
from app.models import Message
from app.users.dependencies import CurrentUser, SessionDep
from fastapi import APIRouter, HTTPException
from app.workouts.models import Workout, WorkoutCreate, WorkoutPublic, WorkoutUpdate, WorkoutsPublic
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
        workouts = session.exec(statement).all()
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
        workouts = session.exec(statement).all()

    return WorkoutsPublic(data=workouts, count=count)

@router.get("/{id}", response_model=WorkoutPublic)
def read_workout(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get workout by ID.
    """
    workout = session.get(Workout, id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if not current_user.is_superuser and (workout.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return workout



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


@router.put("/{id}", response_model=WorkoutPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    workout_in: WorkoutUpdate,
) -> Any:
    """
    Update an workout.
    """
    workout = session.get(Workout, id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if not current_user.is_superuser and (workout.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = workout_in.model_dump(exclude_unset=True)
    workout.sqlmodel_update(update_dict)
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout


@router.delete("/{id}")
def delete_workout(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an workout.
    """
    workout = session.get(Workout, id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if not current_user.is_superuser and (workout.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(workout)
    session.commit()
    return Message(message="Workout deleted successfully")
