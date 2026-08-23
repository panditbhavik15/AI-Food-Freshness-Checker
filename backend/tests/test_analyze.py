"""
Tests for POST /api/v1/analyze endpoint.
"""

def test_analyze_guest_success(client, sample_image_bytes):
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("test_apple.jpg", sample_image_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    result = data["data"]
    assert "food" in result
    assert "freshness" in result
    assert "confidence" in result
    assert "observations" in result
    assert "recommendation" in result
    assert "safety_notice" in result


def test_analyze_authenticated_success(client, auth_headers, test_user, sample_png_bytes):
    response = client.post(
        "/api/v1/analyze",
        headers=auth_headers,
        files={"file": ("test_banana.png", sample_png_bytes, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    result = data["data"]
    assert "id" in result  # Analysis record saved


def test_analyze_invalid_file_type(client):
    invalid_bytes = b"This is a text file, not an image."
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("test.txt", invalid_bytes, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] in ["UNSUPPORTED_FORMAT", "INVALID_IMAGE", "FILE_TOO_LARGE"]
