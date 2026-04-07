"""Tests for the activities endpoints."""

import pytest


def test_get_activities_returns_all_activities(client, test_activities):
    """Test that GET /activities returns all available activities."""
    # Arrange
    expected_count = len(test_activities)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_activities_returns_correct_structure(client, test_activities):
    """Test that activities have the correct structure."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities_data.items():
        assert isinstance(activity_name, str)
        assert set(activity_data.keys()) == required_fields


def test_get_activities_includes_expected_activities(client, test_activities):
    """Test that the response includes known activities."""
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
    ]
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity in expected_activities:
        assert activity in activities_data


def test_get_activities_includes_participants(client, test_activities):
    """Test that activities contain their participants list."""
    # Arrange
    chess_club = "Chess Club"
    expected_initial_participants = 2
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities_data[chess_club]["participants"]) == expected_initial_participants


def test_get_activities_participant_emails_are_strings(client, test_activities):
    """Test that all participants are valid email strings."""
    # Arrange
    
    # Act
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_data in activities_data.values():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant
