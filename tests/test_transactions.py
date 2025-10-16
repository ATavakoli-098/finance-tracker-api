from fastapi.testclient import TestClient

def test_add_and_get_transactions(client: TestClient):
    # create user + category
    user = client.post("/users", json={"name": "Bob"}).json()
    cat = client.post("/categories", json={"name": "Salary", "user_id": user["id"]}).json()

    # add a transaction (income)
    r = client.post(
        "/transactions",
        json={
            "user_id": user["id"],
            "amount": 3000.0,
            "type": "income",
            "category_id": cat["id"],
            "description": "October salary",
            "timestamp": "2025-10-01T10:00:00",
        },
    )
    assert r.status_code == 201
    created = r.json()
    assert created["amount"] == 3000.0
    assert created["type"] == "income"

    # list transactions for user
    r = client.get(f"/transactions?user_id={user['id']}")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["id"] == created["id"]
