"""
Tests for analysis history endpoints (GET /history, GET /history/{id}, DELETE /history/{id}).
"""

def test_get_history_empty(client, auth_headers):
    response = client.get("/api/v1/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 0
    assert data["data"]["items"] == []


def test_get_history_and_detail(client, auth_headers, sample_image_bytes):
    # Perform analysis to populate history
    client.post(
        "/api/v1/analyze",
        headers=auth_headers,
        files={"file": ("apple.jpg", sample_image_bytes, "image/jpeg")},
    )

    # Get history
    history_res = client.get("/api/v1/history", headers=auth_headers)
    assert history_res.status_code == 200
    history_data = history_res.json()["data"]
    assert history_data["total"] == 1
    analysis_id = history_data["items"][0]["id"]

    # Get detail
    detail_res = client.get(f"/api/v1/history/{analysis_id}", headers=auth_headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()["data"]
    assert detail_data["id"] == analysis_id
    assert "observations" in detail_data

    # Delete record
    del_res = client.delete(f"/api/v1/history/{analysis_id}", headers=auth_headers)
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Confirm deletion
    history_after = client.get("/api/v1/history", headers=auth_headers)
    assert history_after.json()["data"]["total"] == 0
