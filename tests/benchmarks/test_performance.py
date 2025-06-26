"""Performance tests for ShortGic URL shortener."""

import pytest
import time
from starlette.testclient import TestClient


def test_health_check_performance(client: TestClient):
    """Test the health check endpoint performance."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "hello" in data


def test_create_link_performance(client: TestClient):
    """Test link creation performance."""
    # Use unique URL to avoid duplicate errors
    unique_url = f"https://example.com/perf-{int(time.time() * 1000000)}"
    response = client.post("/", json={"target": unique_url})
    assert response.status_code == 201
    data = response.json()
    assert "link" in data


def test_access_link_performance(client: TestClient):
    """Test link access/redirect performance."""
    # First create a link to test
    response = client.post("/", json={"target": "https://example.com/perf-redirect"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Test access
    response = client.get(f"/{short_link}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/perf-redirect"


def test_link_info_performance(client: TestClient):
    """Test link info retrieval performance."""
    # First create a link to test
    response = client.post("/", json={"target": "https://example.com/perf-info"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Test info retrieval
    response = client.get(f"/{short_link}/info")
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "https://example.com/perf-info"


def test_delete_link_performance(client: TestClient):
    """Test link deletion performance."""
    # Create a link
    response = client.post("/", json={"target": "https://example.com/perf-delete"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    # Delete the link
    delete_response = client.delete(f"/{short_link}")
    assert delete_response.status_code == 204

    # Verify it's gone
    response = client.get(f"/{short_link}", follow_redirects=False)
    assert response.status_code == 404
