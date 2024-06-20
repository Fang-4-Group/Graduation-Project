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
    assert response.json()  # assure that there are content in response


def test_get_house_info():
    response = client.get("/get_house_info/")
    assert response.status_code == 200
    assert response.json()


def test_item_embedding():
    response = client.get("/item_embedding/")
    assert response.status_code == 200
    assert response.json()
    assert response.json()  # assure that there are content in response


def test_get_name():
    people_id = 1
    response = client.get(f"/get_name/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_sleep_time():
    people_id = 1
    response = client.get(f"/get_sleep_time/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_drink():
    people_id = 1
    response = client.get(f"/get_drink/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_smoke():
    people_id = 1
    response = client.get(f"/get_smoke/{people_id}")
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


def test_get_characters():
    people_id = 1
    response = client.get(f"/get_characters/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_interests():
    people_id = 1
    response = client.get(f"/get_interests/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_size():
    people_id = 1
    response = client.get(f"/get_size/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_fire():
    people_id = 1
    response = client.get(f"/get_fire/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_negotiate():
    people_id = 1
    response = client.get(f"/get_negotiate/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_city():
    people_id = 1
    response = client.get(f"/get_city/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_district():
    people_id = 1
    response = client.get(f"/get_district/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_street():
    people_id = 1
    response = client.get(f"/get_street/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_floor():
    people_id = 1
    response = client.get(f"/get_floor/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_house_type():
    people_id = 1
    response = client.get(f"/get_house_type/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_house_furniture():
    people_id = 1
    response = client.get(f"/get_house_furniture/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_get_house_traffic():
    people_id = 1
    response = client.get(f"/get_house_traffic/{people_id}")
    assert response.status_code == 200
    assert response.json()  # 確保回應有內容


def test_post_user_basic_info():
    sample_data = {
        "Name": "jam",
        "Role": 0,
        "Sleep_Time": 1,
        "Drink": 0,
        "Smoke": 2,
        "Clean": 4,
        "Mbti": "INTJ",
        "Shopping": 0,
        "Movie": 1,
        "Travel": 2,
        "Music": 2,
        "Read": 1,
        "Game": 1,
        "PE": 1,
        "Science": 1,
        "Food": 1,
    }
    response = client.post("/post_user_basic_info/", json=sample_data)
    assert response.status_code == 200


def test_post_house_info():
    sample_data = {
        "People_ID": 1,
        "Size": 10,
        "Fire": 1,
        "Negotiate_Price": 0,
        "City": "臺北市",
        "District": "文山區",
        "Street": "木柵路",
        "Floor": 3,
        "Type": "公寓",
    }
    response = client.post("/post_house_info/", json=sample_data)
    assert response.status_code == 200


def post_house_furniture_info():
    sample_data = {"House_ID": 6, "Furniture": ["沙發", "書桌"]}
    response = client.post("/post_house_furniture_info/", json=sample_data)
    assert response.status_code == 200


def test_post_house_traffic_info():
    sample_data = {"House_ID": 6, "Traffic": ["捷運", "公車"]}
    response = client.post("/post_house_traffic_info/", json=sample_data)
    assert response.status_code == 200


def test_get_pref_house():
    people_id = 2
    response = client.get(f"/get_pref_house_lst/{people_id}")
    assert response.status_code == 200
