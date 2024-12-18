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


def test_get_house_info():
    response = client.get("/get_house_info/")
    assert response.status_code == 200
    assert response.json()


def test_get_name():
    people_id = 1
    response = client.get(f"/get_name/{people_id}")
    assert response.status_code == 200
    assert response.json()


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


def test_embedding_model():
    place_dict = {"data": []}
    response_0 = client.post("/embedding_model/0/1", json=place_dict)
    assert response_0.status_code == 200
    assert response_0.json()


def test_update_user_info():
    sample_data = {
        "People_ID": 1,
        "data": {
            "Name": "湯螞蟻",
            "Sleep_Time": 1,
            "Drink": 1,
            "Smoke": 1,
            "Clean": 1,
            "Mbti": "ENFP",
            "Shopping": 1,
            "Movie": 1,
            "Travel": 1,
            "Music": 1,
            "Read": 1,
            "Game": 1,
            "PE": 1,
            "Science": 1,
            "Food": 1,
        },
    }
    response = client.post("/update_user_info/", json=sample_data)
    assert response.status_code == 200


def test_update_house_info():
    sample_data = {
        "House_ID": 1,
        "Basic": {
            "Size": 10,
            "Fire": 1,
            "Negotiate_Price": 0,
            "City": "更新臺北市",
            "District": "更新文山區",
            "Street": "木柵路",
            "Floor": 3,
            "Type": "公寓",
        },
        "Furniture": ["更新沙發", "更新書桌"],
        "Traffic": ["更新捷運", "更新公車"],
    }
    response = client.post("/update_house_info/", json=sample_data)
    assert response.status_code == 200

def test_update_house_info_recover():
    sample_data = {
        "House_ID": 1,
        "Basic": {
            "Size": 10,
            "Fire": 1,
            "Negotiate_Price": 0,
            "City": "臺北市",
            "District": "文山區",
            "Street": "木柵路",
            "Floor": 3,
            "Type": "公寓",
        },
        "Furniture": ["沙發", "書桌"],
        "Traffic": ["捷運", "公車"],
    }
    response = client.post("/update_house_info/", json=sample_data)
    assert response.status_code == 200


def test_add_recommendation():
    sample_data_0 = {
        "People_ID": 2,
        "Item_ID": [1, 3],
    }
    sample_data_1 = {
        "People_ID": 1,
        "Item_ID": [2, 4],
    }
    response_0 = client.post("/add_recommendation/0", json=sample_data_0)
    response_1 = client.post("/add_recommendation/1", json=sample_data_1)
    assert response_0.status_code == 200
    assert response_1.status_code == 200


def test_get_recommendation():
    response_0 = client.get("/get_recommendation/0/5")
    assert response_0.status_code == 200


def test_add_interaction():
    sample_data_y = {"People_ID": 2, "Options": [7, 8, 10]}
    sample_data_e = {"People_ID": 1, "Options": [2, 4, 10]}

    response_y = client.post("/add_interaction/0", json=sample_data_y)
    response_e = client.post("/add_interaction/1", json=sample_data_e)

    assert response_y.status_code == 200
    assert response_e.status_code == 200


def test_update_viewed():
    sample_data = {"Detail_ID": 2}
    response = client.post("/update_viewed/0", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Update Successfully"}


def test_update_grouped():
    sample_data = {"Detail_ID": 2}
    response = client.post("/update_grouped/0", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Update Successfully"}


def test_update_selected():
    sample_data = {"Detail_ID": 2}
    response = client.post("/update_selected/0", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Update Successfully"}


def test_get_elder_info_by_id():
    house_id = 1
    response = client.get(f"/get_elder_info_by_house_id/{house_id}")
    assert response.status_code == 200
