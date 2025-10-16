from fastapi.testclient import TestClient

def test_create_and_list_categories(client: TestClient):
    # create a user (owner of categories)
    user = client.post("/users", json={"name": "Alice"}).json()

    # create a category
    r = client.post("/categories", json={"name": "Groceries", "user_id": user["id"]})
    assert r.status_code == 201
    cat = r.json()
    assert cat["name"] == "Groceries"
    assert cat["user_id"] == user["id"]

    # list categories for that user
    r = client.get(f"/categories?user_id={user['id']}")
    assert r.status_code == 200
    data = r.json()
    assert any(c["name"] == "Groceries" for c in data)
