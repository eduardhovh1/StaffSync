def _create_department(client, name="Engineering"):
    return client.post("/api/departments/", json={"name": name}).json()


def test_list_employees_empty(client):
    r = client.get("/api/employees/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_employee(client):
    dept = _create_department(client)
    r = client.post(
        "/api/employees/",
        json={
            "name": "Ana Garcia",
            "email": "ana@staffsync.com",
            "department_id": dept["id"],
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["name"] == "Ana Garcia"
    assert body["email"] == "ana@staffsync.com"
    assert body["department_id"] == dept["id"]
    assert "hire_date" in body


def test_create_employee_without_department(client):
    r = client.post(
        "/api/employees/",
        json={"name": "No Dept", "email": "nodept@staffsync.com"},
    )
    assert r.status_code == 201
    assert r.json()["department_id"] is None


def test_create_employee_duplicate_email(client):
    _create_department(client)
    payload = {"name": "Ana", "email": "ana@staffsync.com"}
    assert client.post("/api/employees/", json=payload).status_code == 201
    r = client.post("/api/employees/", json=payload)
    assert r.status_code == 400


def test_create_employee_invalid_email(client):
    r = client.post(
        "/api/employees/", json={"name": "Bad", "email": "not-an-email"}
    )
    assert r.status_code == 422


def test_create_employee_unknown_department(client):
    r = client.post(
        "/api/employees/",
        json={"name": "Ghost", "email": "ghost@staffsync.com", "department_id": 9999},
    )
    assert r.status_code == 400


def test_get_employee(client):
    created = client.post(
        "/api/employees/",
        json={"name": "Carlos Lopez", "email": "carlos@staffsync.com"},
    ).json()
    r = client.get(f"/api/employees/{created['id']}")
    assert r.status_code == 200
    assert r.json()["email"] == "carlos@staffsync.com"


def test_get_employee_not_found(client):
    r = client.get("/api/employees/9999")
    assert r.status_code == 404


def test_update_employee(client):
    created = client.post(
        "/api/employees/",
        json={"name": "Ana", "email": "ana@staffsync.com"},
    ).json()
    r = client.put(f"/api/employees/{created['id']}", json={"name": "Ana Updated"})
    assert r.status_code == 200
    assert r.json()["name"] == "Ana Updated"


def test_update_employee_not_found(client):
    r = client.put("/api/employees/9999", json={"name": "Ghost"})
    assert r.status_code == 404


def test_delete_employee(client):
    created = client.post(
        "/api/employees/",
        json={"name": "Temp", "email": "temp@staffsync.com"},
    ).json()
    r = client.delete(f"/api/employees/{created['id']}")
    assert r.status_code == 204
    assert client.get(f"/api/employees/{created['id']}").status_code == 404


def test_delete_employee_not_found(client):
    r = client.delete("/api/employees/9999")
    assert r.status_code == 404
