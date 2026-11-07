"""Test for GET /api/wilayas."""
import pytest
from django.test import Client


@pytest.mark.django_db
def test_wilayas_endpoint_ordered(client: Client):
    # Seeded by migration (58 wilayas); just check ordering.
    r = client.get("/api/wilayas")
    assert r.status_code == 200
    data = r.json()
    assert data[0]["code"] == 1
    assert data[-1]["code"] == 58
    codes = [x["code"] for x in data]
    assert codes == sorted(codes)
