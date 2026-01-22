import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
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
    yield

@pytest.fixture
def client():
    return TestClient(app)