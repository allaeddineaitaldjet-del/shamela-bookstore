from django.test import Client


def test_root_returns_hello(client: Client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello Al-Shamela Bookstore backend" in response.content


def test_health_returns_ok(client: Client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
