# tests/test_api/test_users.py
def test_create_user(client):
    response = client.post("/orm_users", json={
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "active": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
