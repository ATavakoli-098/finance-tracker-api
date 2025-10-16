from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    r = client.post("/users", json={"name": "Alice"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["name"] == "Alice"
