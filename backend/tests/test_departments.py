def test_list_departments_empty(client):
    r = client.get("/api/departments/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_department(client):
    r = client.post("/api/departments/", json={"name": "Engineering"})
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["name"] == "Engineering"


def test_create_department_invalid(client):
    r = client.post("/api/departments/", json={"name": ""})
    assert r.status_code == 422


def test_get_department(client):
    created = client.post("/api/departments/", json={"name": "Sales"}).json()
    r = client.get(f"/api/departments/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "Sales"


def test_get_department_not_found(client):
    r = client.get("/api/departments/9999")
    assert r.status_code == 404


def test_update_department(client):
    created = client.post("/api/departments/", json={"name": "HR"}).json()
    r = client.put(
        f"/api/departments/{created['id']}", json={"name": "Human Resources"}
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Human Resources"


def test_update_department_not_found(client):
    r = client.put("/api/departments/9999", json={"name": "Ghost"})
    assert r.status_code == 404


def test_delete_department(client):
    created = client.post("/api/departments/", json={"name": "Temp"}).json()
    r = client.delete(f"/api/departments/{created['id']}")
    assert r.status_code == 204
    assert client.get(f"/api/departments/{created['id']}").status_code == 404


def test_delete_department_not_found(client):
    r = client.delete("/api/departments/9999")
    assert r.status_code == 404
