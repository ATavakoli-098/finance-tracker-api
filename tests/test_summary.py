from fastapi.testclient import TestClient

def test_monthly_summary(client: TestClient):
    # user + categories
    user = client.post("/users", json={"name": "Carol"}).json()
    food = client.post("/categories", json={"name": "Food", "user_id": user["id"]}).json()
    rent = client.post("/categories", json={"name": "Rent", "user_id": user["id"]}).json()
    inc  = client.post("/categories", json={"name": "Salary", "user_id": user["id"]}).json()

    # income (2025-10)
    client.post("/transactions", json={
        "user_id": user["id"], "amount": 2000.0, "type": "income",
        "category_id": inc["id"], "description": "Salary",
        "timestamp": "2025-10-01T09:00:00"
    })
    # expenses (2025-10)
    client.post("/transactions", json={
        "user_id": user["id"], "amount": 800.0, "type": "expense",
        "category_id": rent["id"], "description": "Rent",
        "timestamp": "2025-10-02T12:00:00"
    })
    client.post("/transactions", json={
        "user_id": user["id"], "amount": 120.0, "type": "expense",
        "category_id": food["id"], "description": "Groceries",
        "timestamp": "2025-10-05T18:30:00"
    })

    # summary
    r = client.get(f"/summary?user_id={user['id']}&month=2025-10")
    assert r.status_code == 200
    data = r.json()

    assert data["month"] == "2025-10"
    assert data["totals"]["income"] == 2000.0
    assert data["totals"]["expense"] == 920.0
    assert data["totals"]["net"] == 1080.0

    names = {row["category_name"] for row in data["by_category"]}
    assert {"Rent", "Food"}.issubset(names)
