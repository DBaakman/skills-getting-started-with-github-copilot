from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert "participants" in response.json()[expected_activity]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity = app_module.activities[activity_name]
    original_participants = list(activity["participants"])

    if email in activity["participants"]:
        activity["participants"].remove(email)

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activity["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activity["participants"] = original_participants


def test_signup_rejects_when_activity_is_full():
    # Arrange
    activity_name = "Chess Club"
    email = "fullcapacity@mergington.edu"
    activity = app_module.activities[activity_name]
    original_participants = list(activity["participants"])
    activity["participants"] = [
        f"student{i}@mergington.edu" for i in range(activity["max_participants"])
    ]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    finally:
        activity["participants"] = original_participants
