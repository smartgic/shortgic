"""Basic tests for ShortGic URL shortener."""
import pytest
from starlette.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "hello" in data
    assert data["hello"]["msg"] == "welcome on shortgic"


def test_create_short_link(client: TestClient):
    """Test creating a short link."""
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "link" in data
    assert len(data["link"]) >= 5  # Link length varies


def test_redirect(client: TestClient):
    """Test redirect functionality."""
    # First create a link
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Test redirect
    response = client.get(f"/{short_link}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/"


def test_get_link_info(client: TestClient):
    """Test getting link information."""
    # First create a link
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Get link info
    response = client.get(f"/{short_link}/info")
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "https://example.com/"


def test_delete_link(client: TestClient):
    """Test deleting a link."""
    # First create a link
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Delete the link
    response = client.delete(f"/{short_link}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/{short_link}", follow_redirects=False)
    assert response.status_code == 404


def test_duplicate_url(client: TestClient):
    """Test that duplicate URLs are rejected."""
    # Create first link
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 201

    # Try to create the same URL again
    response = client.post("/", json={"target": "https://example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "duplicate_url" in data["detail"]["error"]


def test_invalid_link_format(client: TestClient):
    """Test accessing invalid link formats."""
    # Test too short
    response = client.get("/abc", follow_redirects=False)
    assert response.status_code == 400

    # Test too long
    response = client.get("/abcdefghijk", follow_redirects=False)
    assert response.status_code == 400

    # Test invalid characters
    response = client.get("/abc123!@", follow_redirects=False)
    assert response.status_code == 400


def test_nonexistent_link(client: TestClient):
    """Test accessing a link that doesn't exist."""
    response = client.get("/AAAAA", follow_redirects=False)
    assert response.status_code == 404
