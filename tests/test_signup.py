"""Tests for signup and unregister endpoints."""

import pytest


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_successful_signup(self, client, test_activities, test_emails):
        """Test that a student can successfully sign up for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = test_emails["new"]
        initial_count = len(test_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in test_activities[activity_name]["participants"]
        assert len(test_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_with_activity_name_with_spaces(self, client, test_activities, test_emails):
        """Test signup works with activity names containing spaces."""
        # Arrange
        activity_name = "Programming Class"
        email = test_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in test_activities[activity_name]["participants"]

    def test_signup_duplicate_prevention(self, client, test_activities, test_emails):
        """Test that a student cannot sign up twice for the same activity."""
        # Arrange
        activity_name = "Chess Club"
        email = test_emails["existing"]  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_to_nonexistent_activity(self, client, test_activities, test_emails):
        """Test that signup to non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_emails["new"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_updates_participant_count(self, client, test_activities, test_emails):
        """Test that signup correctly updates the participant count."""
        # Arrange
        activity_name = "Swimming Club"
        email1 = test_emails["new"]
        email2 = test_emails["another_new"]
        initial_count = len(test_activities[activity_name]["participants"])
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert len(test_activities[activity_name]["participants"]) == initial_count + 2


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint."""

    def test_successful_unregister(self, client, test_activities, test_emails):
        """Test that a student can successfully unregister from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = test_emails["existing"]
        initial_count = len(test_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in test_activities[activity_name]["participants"]
        assert len(test_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_nonexistent_activity(self, client, test_activities, test_emails):
        """Test that unregister from non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_emails["existing"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_signed_up(self, client, test_activities, test_emails):
        """Test that unregistering a non-participant returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = test_emails["new"]  # Not signed up
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"

    def test_unregister_with_activity_name_with_spaces(self, client, test_activities, test_emails):
        """Test unregister works with activity names containing spaces."""
        # Arrange
        activity_name = "Basketball Team"
        email = "lucas@mergington.edu"  # Initial participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email not in test_activities[activity_name]["participants"]

    def test_signup_then_unregister_roundtrip(self, client, test_activities, test_emails):
        """Test that signup followed by unregister returns to initial state."""
        # Arrange
        activity_name = "Art Club"
        email = test_emails["new"]
        initial_count = len(test_activities[activity_name]["participants"])
        
        # Act: Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        after_signup_count = len(test_activities[activity_name]["participants"])
        
        # Act: Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        after_unregister_count = len(test_activities[activity_name]["participants"])
        
        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200
        assert after_signup_count == initial_count + 1
        assert after_unregister_count == initial_count
        assert email not in test_activities[activity_name]["participants"]
