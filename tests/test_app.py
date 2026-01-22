import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    # Reset activities to initial state before each test
    initial_activities = {
        "Soccer Team": {
            "description": "Join the school's soccer team and compete in local leagues",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": []
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly matches",
            "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Drama Society": {
            "description": "Participate in acting, stage production, and school plays",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Mathletes": {
            "description": "Compete in math competitions and solve challenging problems",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 10,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    activities.clear()
    activities.update(initial_activities)
    return TestClient(app)


def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_success(client):
    response = client.post("/activities/Soccer%20Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@mergington.edu for Soccer Team" in data["message"]

    # Check that the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Soccer Team"]["participants"]


def test_signup_activity_not_found(client):
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_signed_up(client):
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_unregister_success(client):
    response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]

    # Check that the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]


def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_signed_up(client):
    response = client.delete("/activities/Soccer%20Team/unregister?email=notsignedup@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"