import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state
ORIGINAL_ACTIVITIES = {
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
    },
    "Basketball Team": {
        "description": "Competitive basketball league and training",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and participate in friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["jessica@mergington.edu"]
    },
    "Drama Club": {
        "description": "Stage performances and theatrical productions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts creation",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 18,
        "participants": ["harper@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "mia@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore STEM topics and conduct fascinating experiments",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 24,
        "participants": ["ethan@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to original state before each test.
    This ensures test isolation by preventing state pollution between tests.
    """
    # Reset before test
    activities.clear()
    activities.update({
        key: {"participants": activity["participants"].copy(), **{k: v for k, v in activity.items() if k != "participants"}}
        for key, activity in ORIGINAL_ACTIVITIES.items()
    })
    
    yield
    
    # Cleanup after test (optional but good practice)
    activities.clear()
    activities.update({
        key: {"participants": activity["participants"].copy(), **{k: v for k, v in activity.items() if k != "participants"}}
        for key, activity in ORIGINAL_ACTIVITIES.items()
    })


@pytest.fixture
def client():
    """
    Provides a TestClient with fresh app instance for each test.
    Activities are reset via the reset_activities fixture.
    """
    return TestClient(app)
