import uuid

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_student_cannot_sign_up_twice_for_same_activity():
    email = f"student-{uuid.uuid4().hex[:8]}@mergington.edu"

    first_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"
