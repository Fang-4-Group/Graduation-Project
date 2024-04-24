from fastapi import APIRouter

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
