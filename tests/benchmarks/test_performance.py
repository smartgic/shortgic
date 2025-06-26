"""Performance benchmark tests for ShortGic URL shortener."""
import pytest
from starlette.testclient import TestClient


def test_health_check_performance(benchmark, client: TestClient):
    """Benchmark the health check endpoint performance."""
    def health_check():
        response = client.get("/")
        assert response.status_code == 200
        return response

    result = benchmark(health_check)
    assert result.status_code == 200


def test_create_link_performance(benchmark, client: TestClient):
    """Benchmark link creation performance."""
    import time
    def create_link():
        # Use unique URL to avoid duplicate errors
        unique_url = f"https://example.com/benchmark-{int(time.time() * 1000000)}"
        response = client.post("/", json={"target": unique_url})
        assert response.status_code == 201
        return response

    result = benchmark(create_link)
    assert result.status_code == 201
    data = result.json()
    assert "link" in data


def test_access_link_performance(benchmark, client: TestClient):
    """Benchmark link access/redirect performance."""
    # First create a link to benchmark
    response = client.post("/", json={"target": "https://example.com/benchmark-redirect"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    def access_link():
        response = client.get(f"/{short_link}", follow_redirects=False)
        assert response.status_code == 302
        return response

    result = benchmark(access_link)
    assert result.status_code == 302


def test_link_info_performance(benchmark, client: TestClient):
    """Benchmark link info retrieval performance."""
    # First create a link to benchmark
    response = client.post("/", json={"target": "https://example.com/benchmark-info"})
    assert response.status_code == 201
    data = response.json()
    short_link = data["link"]

    def get_link_info():
        response = client.get(f"/{short_link}/info")
        assert response.status_code == 200
        return response

    result = benchmark(get_link_info)
    assert result.status_code == 200


def test_delete_link_performance(benchmark, client: TestClient):
    """Benchmark link deletion performance."""
    def create_and_delete_link():
        # Create a link
        response = client.post("/", json={"target": "https://example.com/benchmark-delete"})
        assert response.status_code == 201
        data = response.json()
        short_link = data["link"]

        # Delete the link
        delete_response = client.delete(f"/{short_link}")
        assert delete_response.status_code == 204
        return delete_response

    result = benchmark(create_and_delete_link)
    assert result.status_code == 204
