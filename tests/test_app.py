"""
Backend tests for FastAPI application using AAA (Arrange-Act-Assert) pattern.
Tests cover all endpoints: GET /, GET /activities, POST signup, DELETE participants.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing TestClient with fresh app state."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirect_to_static(self, client):
        """
        Arrange: Initial state ready
        Act: Make GET request to /
        Assert: Should redirect to /static/index.html
        """
        response = client.get("/", follow_redirects=False)

        assert response.status_code == 307


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_success(self, client):
        """
        Arrange: Client ready with fresh app
        Act: Make GET request to /activities
        Assert: Should return all 9 activities with correct structure
        """
        response = client.get("/activities")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        
        # Validate structure of first activity
        first_activity = data.get("Chess Club")
        assert first_activity is not None
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """
        Arrange: Client ready, prepare email for signup
        Act: Make POST request to signup for existing activity
        Assert: Should add participant and return 200
        """
        email = "student@example.com"
        activity = "Chess Club"

        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_activity_not_found(self, client):
        """
        Arrange: Prepare request for non-existent activity
        Act: Make POST request to non-existent activity
        Assert: Should return 404
        """
        email = "student@example.com"
        activity = "NonExistentActivity"

        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response.status_code == 404

    def test_signup_already_enrolled(self, client):
        """
        Arrange: Sign up student to activity, then attempt duplicate signup
        Act: Make POST request with same email to same activity twice
        Assert: Second signup should return 400
        """
        email = "student@example.com"
        activity = "Chess Club"

        # First signup - should succeed
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response1.status_code == 200

        # Duplicate signup - should fail
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        assert response2.status_code == 400

    def test_signup_adds_participant_to_list(self, client):
        """
        Arrange: Prepare to signup and verify activity state
        Act: Sign up student, then get activities list
        Assert: Student email should appear in participants list
        """
        email = "newstudent@example.com"
        activity = "Basketball Team"

        client.post(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        activities = response.json()

        assert email in activities[activity]["participants"]


class TestDeleteParticipantEndpoint:
    """Tests for DELETE /activities/{activity_name}/participants endpoint"""

    def test_delete_participant_success(self, client):
        """
        Arrange: Sign up student first
        Act: Delete student from activity
        Assert: Should return success message and 200
        """
        email = "student@example.com"
        activity = "Tennis Club"

        # First signup
        client.post(f"/activities/{activity}/signup?email={email}")

        # Then delete
        response = client.delete(
            f"/activities/{activity}/participants?email={email}"
        )

        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

    def test_delete_activity_not_found(self, client):
        """
        Arrange: Prepare delete request for non-existent activity
        Act: Make DELETE request to non-existent activity
        Assert: Should return 404
        """
        email = "student@example.com"
        activity = "NonExistentActivity"

        response = client.delete(
            f"/activities/{activity}/participants?email={email}"
        )

        assert response.status_code == 404

    def test_delete_participant_not_found(self, client):
        """
        Arrange: Prepare delete request for non-enrolled student
        Act: Make DELETE request to remove student not in activity
        Assert: Should return 404
        """
        email = "notstudent@example.com"
        activity = "Drama Club"

        response = client.delete(
            f"/activities/{activity}/participants?email={email}"
        )

        assert response.status_code == 404

    def test_delete_removes_participant_from_list(self, client):
        """
        Arrange: Sign up student first
        Act: Delete student, then get activities
        Assert: Student email should not appear in participants list
        """
        email = "removeme@example.com"
        activity = "Art Studio"

        # Signup
        client.post(f"/activities/{activity}/signup?email={email}")

        # Delete
        client.delete(
            f"/activities/{activity}/participants?email={email}"
        )

        # Verify removed
        response = client.get("/activities")
        activities = response.json()

        assert email not in activities[activity]["participants"]
