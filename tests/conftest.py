"""Pytest configuration and fixtures."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def test_activities(monkeypatch):
    """
    Provide a fresh copy of activities for each test.
    
    This fixture uses monkeypatch to replace the module-level activities
    dictionary with a deep copy, ensuring tests don't mutate shared state.
    """
    # Arrange: Create a deep copy of the original activities
    fresh_activities = copy.deepcopy(activities)
    
    # Arrange: Replace the module-level activities with our copy
    monkeypatch.setattr("src.app.activities", fresh_activities)
    
    return fresh_activities


@pytest.fixture
def test_emails():
    """Provide common test email addresses."""
    return {
        "existing": "michael@mergington.edu",
        "new": "test.student@mergington.edu",
        "another_new": "another.student@mergington.edu",
    }
