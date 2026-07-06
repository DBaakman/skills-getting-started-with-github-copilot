from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_from_activity():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    app_module.activities[activity_name]["participants"].append(email)

    try:
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in app_module.activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    finally:
        if email in app_module.activities[activity_name]["participants"]:
            app_module.activities[activity_name]["participants"].remove(email)
