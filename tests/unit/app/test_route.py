from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_test_create():
    response = client.get("/test_create/")
    assert response.status_code == 200


def test_test_select():
    response = client.get("/test_select/")
    assert response.status_code == 200


def test_test_drop():
    response = client.get("/test_drop/")
    assert response.status_code == 200


def test_test_create_img():
    response = client.get("/test_create_img/")
    assert response.status_code == 200


def test_show_img():
    response = client.get("/show_img/")
    assert response.status_code == 200


def test_test_drop_img():
    response = client.get("/test_drop_img/")
    assert response.status_code == 200


def test_test_insert_mongo():
    response = client.get("/test_insert_mongo/")
    assert response.status_code == 200


def test_test_select_mongo():
    response = client.get("/test_select_mongo/")
    assert response.status_code == 200


def test_test_drop_mongo():
    response = client.get("/test_drop_mongo/")
    assert response.status_code == 200


def test_pg_init():
    response = client.get("/pg_init/")
    assert response.status_code == 200


def test_pg_init_test():
    response = client.get("/pg_init_test/")
    assert response.status_code == 200


def test_mongodb_init():
    response = client.get("/mongo_init/")
    assert response.status_code == 200


def test_get_young_info():
    response = client.get("/get_young_info/")
    assert response.status_code == 200
    assert response.json()  # assure that there are content in response


def test_get_elder_info():
    response = client.get("/get_elder_info/")
    assert response.status_code == 200
    assert response.json()


def test_get_preference_house_place():
    preference_id = 1
    response = client.get(f"/get_preference_house_place/{preference_id}")
    assert response.status_code == 200
    assert response.json()


def test_get_district_geocoding():
    city = "臺北市"
    district = "文山區"
    response = client.get(f"/get_district_geocoding/{city}/{district}")
    assert response.status_code == 200
    assert response.json()


def test_embedding():
    k_mean = 1
    n_clusters = 3
    par = f"?k_mean={k_mean}&n_clusters={n_clusters}"
    response = client.get(f"user_embedding/{par}")
    assert response.status_code == 200
