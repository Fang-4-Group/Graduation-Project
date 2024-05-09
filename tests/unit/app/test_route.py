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
<<<<<<< HEAD
    assert response.json()  # assure that there are content in response
=======
    assert response.json()  # 確保回應有內容
>>>>>>> c758ff6 (add apis)


def test_get_preference_furniture():
    preference_id = 1
    response = client.get(f"/get_preference_furniture/{preference_id}")
    assert response.status_code == 200
<<<<<<< HEAD
    assert response.json()  # assure that there are content in response
=======
    assert response.json()  # 確保回應有內容
>>>>>>> c758ff6 (add apis)


def test_get_preference_house_place():
    preference_id = 1
    response = client.get(f"/get_preference_house_place/{preference_id}")
    assert response.status_code == 200
<<<<<<< HEAD
    assert response.json()  # assure that there are content in response
=======
    assert response.json()  # 確保回應有內容

def test_get_sleep_time():
    people_id = 1
    response = client.get(f"/get_sleep_time/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_get_drink_or_smoke():
    people_id = 1
    response = client.get(f"/get_drink_or_smoke/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_get_clean_habit():
    people_id = 1
    response = client.get(f"/get_clean_habit/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_get_mbti():
    people_id = 1
    response = client.get(f"/get_mbti/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_get_interests():
    people_id = 1
    response = client.get(f"/get_interests/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_update_sleep_time():
    people_id = 1
    new_sleep_time=5
    response = client.get(f"/update_sleep_time/{people_id},{new_sleep_time}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_update_drink_or_smoke():
    people_id = 1
    new_drink_or_smoke=5
    response = client.get(f"/update_drink_or_smoke/{people_id},{new_drink_or_smoke}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_update_clean_habit():
    people_id = 1
    new_clean=5
    response = client.get(f"/update_clean_habit/{people_id},{new_clean}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_update_mbti():
    people_id = 1
    new_mbti='CUTE'
    response = client.get(f"/update_mbti/{people_id},{new_mbti}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容
    
def test_add_preference_house_furniture():
    preference_id = 1
    new_furniture=['大餐桌','小餐桌']
    response = client.get(f"/add_preference_house_furniture/{preference_id},{new_furniture}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_add_preference_house_place():
    preference_id = 1
    new_place=['金山區','三芝區']
    response = client.get(f"/add_preference_house_place/{preference_id},{new_place}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容

def test_update_integer_field():
    column_name = 'shopping'
    people_id=1
    new_value=1
    response = client.get(f"/add_preference_house_place/{column_name},{people_id},{new_value}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容
>>>>>>> c758ff6 (add apis)
