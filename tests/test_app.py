"""Backend tests for the Mergington High School activities API."""

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange & Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Soccer Team" in data
    assert "description" in data["Chess Club"]


def test_signup_for_activity_succeeds():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Art Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email in activities["Art Club"]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    email = "repeat@mergington.edu"
    client.post("/activities/Debate Team/signup", params={"email": email})

    # Act
    response = client.post("/activities/Debate Team/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_unknown_activity_returns_404():
    # Act
    response = client.post("/activities/Nonexistent Club/signup", params={"email": "x@mergington.edu"})

    # Assert
    assert response.status_code == 404
