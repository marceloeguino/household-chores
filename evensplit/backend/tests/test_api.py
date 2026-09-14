import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    # Fresh in-memory SQLite database per test, wired in via dependency override
    # so tests never touch the real evensplit.db file.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def seed_members(client):
    names = ["Alex", "Sam", "Jordan"]
    return {n: client.post("/members", json={"name": n}).json()["id"] for n in names}


def test_list_members_starts_empty_until_seeded(client):
    # Startup event seeds Alex/Sam/Jordan against the *app-level* engine, not
    # this test's isolated in-memory db, so this db starts empty.
    assert client.get("/members").json() == []


def test_add_member(client):
    res = client.post("/members", json={"name": "Riley"})
    assert res.status_code == 201
    assert res.json()["name"] == "Riley"
    assert len(client.get("/members").json()) == 1


def test_add_expense_and_balances(client):
    members = seed_members(client)
    res = client.post(
        "/expenses",
        json={
            "description": "Dinner",
            "amount": 90,
            "paid_by": members["Alex"],
            "participants": [members["Alex"], members["Sam"], members["Jordan"]],
        },
    )
    assert res.status_code == 201

    balances = {b["name"]: b["balance"] for b in client.get("/balances").json()}
    assert balances["Alex"] == 60.0
    assert balances["Sam"] == -30.0
    assert balances["Jordan"] == -30.0


def test_add_expense_rejects_unknown_member(client):
    res = client.post(
        "/expenses",
        json={"description": "x", "amount": 10, "paid_by": 999, "participants": [999]},
    )
    assert res.status_code == 422


def test_delete_expense(client):
    members = seed_members(client)
    created = client.post(
        "/expenses",
        json={
            "description": "Snacks",
            "amount": 20,
            "paid_by": members["Alex"],
            "participants": [members["Alex"], members["Sam"]],
        },
    ).json()

    res = client.delete(f"/expenses/{created['id']}")
    assert res.status_code == 204
    assert client.get("/expenses").json() == []


def test_delete_missing_expense_404(client):
    res = client.delete("/expenses/9999")
    assert res.status_code == 404


def test_expenses_persist_across_requests(client):
    # Regression test for the mock->real-DB swap: data must survive
    # between separate requests within the same test client/session.
    members = seed_members(client)
    client.post(
        "/expenses",
        json={
            "description": "Rent",
            "amount": 300,
            "paid_by": members["Sam"],
            "participants": [members["Alex"], members["Sam"], members["Jordan"]],
        },
    )
    expenses = client.get("/expenses").json()
    assert len(expenses) == 1
    assert expenses[0]["description"] == "Rent"
