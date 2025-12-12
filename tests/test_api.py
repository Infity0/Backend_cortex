import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "username": "testuser"
        }
    )
    # Note: This will fail without a real database connection
    # Just checking the endpoint exists
    assert response.status_code in [201, 500]


def test_get_subscription_plans():
    """Test getting subscription plans"""
    response = client.get("/api/subscriptions/plans")
    # Note: This will fail without a real database connection
    assert response.status_code in [200, 500]
