from fastapi import APIRouter
from fastapi.responses import FileResponse

from database.seeds.mongo_api_for_testing import MongoDBClient
from database.seeds.pg_api_for_testing import DatabaseClient

router = APIRouter()


@router.get("/test_create/")
async def test_create():
    client = DatabaseClient()
    result = await client.test_create_fun()
    return result


@router.get("/test_select/")
async def test_select():
    client = DatabaseClient()
    result = await client.test_select_fun()
    return result


@router.get("/test_drop/")
async def test_drop():
    client = DatabaseClient()
    result = await client.test_drop_fun()
    return result


@router.get("/test_create_img/")
async def test_create_img():
    client = DatabaseClient()
    result = await client.test_create_img_fun()
    return result


@router.get("/show_img/")
async def show_img():
    client = DatabaseClient()
    data = await client.test_select_img_fun()
    return FileResponse(data["message"][0]["path"])


@router.get("/test_drop_img/")
async def test_drop_img():
    client = DatabaseClient()
    result = await client.test_drop_img_fun()
    return result


# MongoDB


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
