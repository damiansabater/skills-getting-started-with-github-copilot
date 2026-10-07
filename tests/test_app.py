import uuid

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Return a FastAPI test client with a clean in-memory activity store."""
    original_activities = {
        name: {
            **details,
            "participants": list(details["participants"]),
        }
        for name, details in activities.items()
    }

    activities.clear()
    activities.update(original_activities)

    with TestClient(app) as test_client:
        yield test_client


def test_student_cannot_sign_up_twice_for_same_activity(client):
    # Arrange
    email = f"student-{uuid.uuid4().hex[:8]}@mergington.edu"

    # Act
    first_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_get_activities_returns_activity_data(client):
    # Arrange
    # no setup required beyond the client fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
