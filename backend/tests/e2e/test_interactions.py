import httpx

def test_get_interactions_returns_200(client: httpx.Client) -> None:
    """E2E test: GET /interactions/ returns status 200"""
    response = client.get("/interactions/")
    assert response.status_code == 200

def test_get_interactions_response_items_have_expected_fields(client: httpx.Client) -> None:
    """E2E test: Response items contain expected fields"""
    response = client.get("/interactions/")
    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]
    assert "item_id" in data[0]
    assert "created_at" in data[0]