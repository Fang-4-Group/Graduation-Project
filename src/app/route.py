from fastapi import APIRouter
from fastapi.responses import FileResponse

from database.migrations.mongodb_init import MongoDBInitClient
from database.migrations.pg_CRUD import PosgresqClient
from database.migrations.posgresql_init import PosgresqlInitClient
from database.seeds.mongo_api_for_testing import MongoDBClient
from database.seeds.pg_api_for_testing import PosgresqTestClient

router = APIRouter()


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
    return {
        "create table": f"{response_c['message']}",
        "add FK": f"{response_a['message']}",
        "insert data": f"{response_i['message']}",
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


@router.get("/mongo_init_test/")
async def mongodb_init_test():
    client = MongoDBInitClient()
    response = await client.get_data_by_group_id(
        "B1c2d3e4f5g67890hijklmnopqrstuvwx"
    )  # noqa
    return response


# Posgresql CRUD


@router.get("/get_young_info/")
async def get_young_info():
    client = PosgresqClient()
    result = await client.get_young_info()
    return result


@router.get("/get_preference_furniture/{preference_id}")
async def get_preference_furniture(preference_id: int):
    client = PosgresqClient()
    result = await client.get_preference_furniture(preference_id)
    return result


@router.get("/get_preference_house_place/{preference_id}")
async def get_preference_house_place(preference_id: int):
    client = PosgresqClient()
    result = await client.get_preference_house_place(preference_id)
    return result
