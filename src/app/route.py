from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from starlette.responses import RedirectResponse

from database.migrations.mongodb_init import MongoDBInitClient
from database.migrations.pg_CRUD import PosgresqClient
from database.migrations.posgresql_init import PosgresqlInitClient
from database.seeds.mongo_api_for_testing import MongoDBClient
from database.seeds.pg_api_for_testing import PosgresqTestClient
from src.chatbot.database import get_group_chat_records_by_id
from src.data_pipeline.item_embedding import ItemEmbedding
from src.data_pipeline.model import EmbeddingModel
from src.data_pipeline.prediction import Prediction
from src.data_pipeline.user_embedding import UserEmbedding

from ..services.google_oidc.oidc import OIDCService

router = APIRouter()
oidc_service = OIDCService()

jinja_env = Environment(loader=FileSystemLoader("src/templates"))

# Posgresql Test


@router.get("/test_create/")
async def test_create():
    client = PosgresqTestClient()
    result = await client.test_create_fun()
    return result


@router.get("/test_select/")
async def test_select():
    client = PosgresqTestClient()
    result = await client.test_select_fun()
    return result


@router.get("/test_drop/")
async def test_drop():
    client = PosgresqTestClient()
    result = await client.test_drop_fun()
    return result


@router.get("/test_create_img/")
async def test_create_img():
    client = PosgresqTestClient()
    result = await client.test_create_img_fun()
    return result


@router.get("/show_img/")
async def show_img():
    client = PosgresqTestClient()
    data = await client.test_select_img_fun()
    return FileResponse(data["message"][0]["path"])


@router.get("/test_drop_img/")
async def test_drop_img():
    client = PosgresqTestClient()
    result = await client.test_drop_img_fun()
    return result


# MongoDB Test


@router.get("/test_insert_mongo/")
async def test_insert_mg():
    client = MongoDBClient()
    result = await client.test_insert_fun()
    return result


@router.get("/test_select_mongo/")
async def test_select_mg():
    client = MongoDBClient()
    result = await client.test_select_fun()
    return result


@router.get("/test_drop_mongo/")
async def test_drop_mg():
    client = MongoDBClient()
    result = await client.test_drop_fun()
    return result


# posgresql init


@router.get("/pg_init/")
async def posgresql_init():
    client = PosgresqlInitClient()
    response_c = await client.create_table()
    response_a = await client.add_fk_setting()
    response_i = await client.insert_data()
    response_d = await client.insert_district_data()
    return {
        "create table": f"{response_c['message']}",
        "add FK": f"{response_a['message']}",
        "insert data": f"{response_i['message']}",
        "insert district data": f"{response_d['message']}",
    }


@router.get("/pg_init_test/")
async def posgresql_init_test():
    client = PosgresqlInitClient()
    response = await client.select_house_data()
    return response


# mongodb init


@router.get("/mongo_init/")
async def mongodb_init():
    client = MongoDBInitClient()
    response = await client.insert_data()
    return response


# Posgresql CRUD


@router.get("/get_young_info/")
async def get_young_info(
    amount: int = Query(None, description="指定要獲取的人員數量")
):  # noqa
    client = PosgresqClient()
    result = await client.get_young_info(amount=amount)
    return result


@router.get("/get_elder_info/")
async def get_elder_info():
    client = PosgresqClient()
    result = await client.get_elder_info()
    return result


@router.get("/get_preference_house_place/{preference_id}")
async def get_preference_house_place(preference_id: int):
    client = PosgresqClient()
    result = await client.get_preference_house_place(preference_id)
    return result


@router.get("/get_district_geocoding/{city}/{district}")
async def get_district_geocoding(city: str, district: str):
    client = PosgresqClient()
    result = await client.get_district_geocoding(city, district)
    return result


@router.post("/post_user_basic_info/")
async def post_user_basic_info(user_data: dict):
    client = PosgresqClient()
    result = await client.post_user_basic_info(user_data)
    return result


@router.post("/post_house_info/")
async def post_house_info(house_data: dict):
    client = PosgresqClient()
    result = await client.post_house_info(house_data)
    return result


@router.post("/post_house_furniture_info/")
async def post_house_furniture_info(house_furn_data: dict):
    client = PosgresqClient()
    result = await client.post_house_furniture_info(house_furn_data)
    return result


@router.post("/post_house_traffic_info/")
async def post_house_traffic_info(house_traffic_data: dict):
    client = PosgresqClient()
    result = await client.post_house_traffic_info(house_traffic_data)
    return result


@router.post("/update_user_info/")
async def update_user_info(user_update_data: dict):
    client = PosgresqClient()
    result = await client.update_user_info(user_update_data)
    return result


@router.post("/update_house_info/")
async def update_house_info(house_update_data: dict):
    client = PosgresqClient()
    result = await client.update_house_info(house_update_data)
    return result


# @router.post("/update_house_furniture_info/")
# async def update_house_furniture_info(house_furniture_update_data: dict):
# client = PosgresqClient()
# result = await client.update_house_furniture_info(house_furniture_update_data) # noqa
# return result


# @router.post("/update_house_traffic_info/")
# async def update_house_furniture_info(house_furniture_update_data: dict):
# client = PosgresqClient()
# result = await client.update_house_
# furniture_info(house_furniture_update_data)


# @router.post("/update_preference_house_place/")
# async def update_house_furniture_info(house_furniture_update_data: dict):
#     client = PosgresqClient()
#     result = await client.update_
# house_furniture_info(house_furniture_update_data) #noqa
#     return result


# Googel OIDC Login
@router.get("/google-oidc/")
async def root(request: Request):
    try:
        home_temp = jinja_env.get_template("homepage.html")
        html_content = home_temp.render()
        return HTMLResponse(content=html_content)
    except TemplateNotFound as e:
        return HTTPException(status_code=404, detail=f"Template not found: {e}")  # noqa


@router.get("/google-oidc/login")
async def login(request: Request):
    authorization_url, state = oidc_service.get_authorization_url()
    request.session["state"] = state
    return RedirectResponse(authorization_url)


@router.get("/google-oidc/auth")
async def auth(request: Request):
    state = request.session.get("state")
    if not state:
        raise HTTPException(
            status_code=400, detail="State not found in session"
        )  # noqa

    authorization_response = str(request.url)

    try:
        oidc_service.fetch_token(authorization_response)
        credentials = oidc_service.flow.credentials
        request.session["access_token"] = credentials.token
        userinfo = oidc_service.verify_id_token(credentials.id_token)
        template = jinja_env.get_template("profile.html")
        html_content = template.render(userinfo=userinfo)
        return HTMLResponse(content=html_content)
    except ValueError as e:
        return HTMLResponse(
            content=f"Error: Invalid token: {e}", status_code=400
        )  # noqa


# Embedding


@router.get("/user_embedding/")
async def embedding(k_mean: bool = 0, n_clusters: int = 3):
    client = UserEmbedding()
    result = client.embedding(k_mean, n_clusters)
    return result


@router.get("/get_house_info/")
async def get_house_info(city: str = Query(None), district: str = Query(None)):
    client = PosgresqClient()
    result = await client.get_house_info(city=city, district=district)
    return result


@router.post("/item_embedding/")
async def item_embedding(place_dict: dict = None):
    client = ItemEmbedding()
    result = await client.item_embedding(place_dict["data"])
    return result


@router.get("/get_name/{people_id}")
async def get_name(people_id: int):
    client = PosgresqClient()
    result = await client.get_name(people_id)
    return result


@router.get("/get_sleep_time/{people_id}")
async def get_sleep_time(people_id: int):
    client = PosgresqClient()
    result = await client.get_sleep_time(people_id)
    return result


@router.get("/get_drink/{people_id}")
async def get_drink(people_id: int):
    client = PosgresqClient()
    result = await client.get_drink(people_id)
    return result


@router.get("/get_smoke/{people_id}")
async def get_smoke(people_id: int):
    client = PosgresqClient()
    result = await client.get_smoke(people_id)
    return result


@router.get("/get_clean_habit/{people_id}")
async def get_clean_habit(people_id: int):
    client = PosgresqClient()
    result = await client.get_clean_habit(people_id)
    return result


@router.get("/get_mbti/{people_id}")
async def get_mbti(people_id: int):
    client = PosgresqClient()
    result = await client.get_mbti(people_id)
    return result


@router.get("/get_characters/{people_id}")
async def get_characters(people_id: int):
    client = PosgresqClient()
    result = await client.get_characters(people_id)
    return result


@router.get("/get_interests/{people_id}")
async def get_interests(people_id: int):
    client = PosgresqClient()
    result = await client.get_interests(people_id)
    return result


@router.get("/get_size/{people_id}")
async def get_size(people_id: int):
    client = PosgresqClient()
    result = await client.get_size(people_id)
    return result


@router.get("/get_fire/{people_id}")
async def get_fire(people_id: int):
    client = PosgresqClient()
    result = await client.get_fire(people_id)
    return result


@router.get("/get_negotiate/{people_id}")
async def get_negotiate(people_id: int):
    client = PosgresqClient()
    result = await client.get_negotiate(people_id)
    return result


@router.get("/get_city/{people_id}")
async def get_city(people_id: int):
    client = PosgresqClient()
    result = await client.get_city(people_id)
    return result


@router.get("/get_district/{people_id}")
async def get_district(people_id: int):
    client = PosgresqClient()
    result = await client.get_district(people_id)
    return result


@router.get("/get_street/{people_id}")
async def get_street(people_id: int):
    client = PosgresqClient()
    result = await client.get_street(people_id)
    return result


@router.get("/get_floor/{people_id}")
async def get_floor(people_id: int):
    client = PosgresqClient()
    result = await client.get_floor(people_id)
    return result


@router.get("/get_house_type/{people_id}")
async def get_house_type(people_id: int):
    client = PosgresqClient()
    result = await client.get_house_type(people_id)
    return result


@router.get("/get_house_furniture/{people_id}")
async def get_house_furniture(people_id: int):
    client = PosgresqClient()
    result = await client.get_house_furniture(people_id)
    return result


@router.get("/get_house_traffic/{people_id}")
async def get_house_traffic(people_id: int):
    client = PosgresqClient()
    result = await client.get_house_traffic(people_id)
    return result


@router.post("/add_recommendation/{type}")
async def add_recommendation(type: int, recommendation_info: dict):
    client = PosgresqClient()
    result = await client.add_recommendation(type, recommendation_info)
    return result


@router.post("/get_recommendation/{type}")
async def get_recommendation(type: int, condition: dict = None):
    item_ids = condition["Item_ID"]
    client = PosgresqClient()
    result = await client.get_recommendation(type, item_ids)
    return result


# ToDo: Complete  API (edit and insert) outlined in ticket [GP102]


# Prediction


@router.get("/get_pref_house_lst/{people_id}")
async def get_pref_house_lst(people_id: int):
    client = Prediction()
    result = await client.get_pref_house_lst(people_id)
    return result


# Model
@router.post("/embedding_model/{target}")
async def embeddingModel(target: int, place_dict: dict = None):
    model = EmbeddingModel(target, place_dict)
    result = await model.run()
    return result


# API for GAI
@router.get("/get_group_chat_records/{group_id}")
async def get_group_chat_records(group_id: str):
    result = get_group_chat_records_by_id(group_id)
    return result
