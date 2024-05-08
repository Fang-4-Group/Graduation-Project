from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_create_status_code():
    response = client.get("/test_create/")
    assert response.status_code == 200


def test_select_status_code():
    response = client.get("/test_select/")
    assert response.status_code == 200


def test_drop_status_code():
    response = client.get("/test_drop/")
    assert response.status_code == 200


def test_create_img_status_code():
    response = client.get("/test_create_img/")
    assert response.status_code == 200


def show_img_status_code():
    response = client.get("/show_img/")
    assert response.status_code == 200


def test_drop_img_status_code():
    response = client.get("/test_drop_img/")
    assert response.status_code == 200


def test_insert_mongo_status_code():
    response = client.get("/test_insert_mongo/")
    assert response.status_code == 200


def test_select_mongo_status_code():
    response = client.get("/test_select_mongo/")
    assert response.status_code == 200


def test_drop_mongo_status_code():
    response = client.get("/test_drop_mongo/")
    assert response.status_code == 200


def test_pg_init_status_code():
    response = client.get("/pg_init/")
    assert response.status_code == 200


def test_pg_init_test_status_code():
    response = client.get("/pg_init_test/")
    assert response.status_code == 200


def test_mongodb_init_status_code():
    response = client.get("/mongo_init/")
    assert response.status_code == 200


def test_mongodb_init_test_status_code():
    response = client.get("/mongo_init_test/")
    assert response.status_code == 200


def test_get_young_info():
    response = client.get("/get_young_info/")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_preference_furniture():
    preference_id = 1
    response = client.get(f"/get_preference_furniture/{preference_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_preference_house_place():
    preference_id = 1
    response = client.get(f"/get_preference_house_place/{preference_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容
