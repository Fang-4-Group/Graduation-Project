from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_create_status_code():
    response = client.get("/test_create/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_select_status_code():
    response = client.get("/test_select/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_drop_status_code():
    response = client.get("/test_drop/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_create_img_status_code():
    response = client.get("/test_create_img/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def show_img_status_code():
    response = client.get("/show_img/")
    assert response.status_code == 200
    # assert response.json()["status"] == 200


def test_drop_img_status_code():
    response = client.get("/test_drop_img/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_insert_mongo_status_code():
    response = client.get("/test_insert_mongo/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_select_mongo_status_code():
    response = client.get("/test_select_mongo/")
    assert response.status_code == 200
    assert response.json()["status"] == 200


def test_drop_mongo_status_code():
    response = client.get("/test_drop_mongo/")
    assert response.status_code == 200
    assert response.json()["status"] == 200
