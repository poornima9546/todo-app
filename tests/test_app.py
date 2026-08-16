import sys
import os

# Add the app directory to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app")
    )
)

import app


def test_home():
    app.app.testing = True
    client = app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "To-Do Application is running"


def test_health():
    app.app.testing = True
    client = app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_todo_requires_title():
    app.app.testing = True
    client = app.app.test_client()

    response = client.post(
        "/todos",
        json={
            "description": "Test todo"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"
