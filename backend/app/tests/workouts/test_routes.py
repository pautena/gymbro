from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.workouts import create_random_workout


def test_read_workouts(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_workout(db)
    create_random_workout(db)
    response = client.get(
        f"{settings.API_V1_STR}/workouts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_read_workout(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    response = client.get(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(workout.id)


def test_read_workout_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        f"{settings.API_V1_STR}/workouts/{non_existent_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Workout not found"


def test_read_workout_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    response = client.get(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_create_workout(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Test Workout", "notes": "Test Note"}
    response = client.post(
        f"{settings.API_V1_STR}/workouts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["notes"] == data["notes"]


def test_update_workout(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    data = {"name": "Updated Workout"}
    response = client.put(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=superuser_token_headers,
        json=data,
    )
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]


def test_update_workout_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    data = {"name": "Non-existent Workout"}
    response = client.put(
        f"{settings.API_V1_STR}/workouts/{non_existent_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Workout not found"


def test_update_workout_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    data = {"name": "Unauthorized Update"}
    response = client.put(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_workout(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    response = client.delete(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Workout deleted successfully"


def test_delete_workout_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(
        f"{settings.API_V1_STR}/workouts/{non_existent_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Workout not found"


def test_delete_workout_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    workout = create_random_workout(db)
    response = client.delete(
        f"{settings.API_V1_STR}/workouts/{workout.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
