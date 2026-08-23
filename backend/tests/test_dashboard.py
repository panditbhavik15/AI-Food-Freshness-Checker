"""
Tests for dashboard stats endpoint (GET /dashboard).
"""

def test_get_dashboard_empty(client, auth_headers):
    response = client.get("/api/v1/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    stats = data["data"]
    assert stats["total_scans"] == 0
    assert stats["top_foods"] == []


def test_get_dashboard_populated(client, auth_headers, sample_image_bytes):
    # Perform two analyses
    client.post(
        "/api/v1/analyze",
        headers=auth_headers,
        files={"file": ("img1.jpg", sample_image_bytes, "image/jpeg")},
    )
    client.post(
        "/api/v1/analyze",
        headers=auth_headers,
        files={"file": ("img2.jpg", sample_image_bytes, "image/jpeg")},
    )

    response = client.get("/api/v1/dashboard", headers=auth_headers)
    assert response.status_code == 200
    stats = response.json()["data"]
    assert stats["total_scans"] == 2
    assert len(stats["recent_analyses"]) == 2
