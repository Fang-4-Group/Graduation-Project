from fastapi import APIRouter

from database.seeds import mongo_api_for_testing as mg_api_t
from database.seeds import pg_api_for_testing as pg_api_t

router = APIRouter()


@router.get("/test_create/")
async def test_create():
    result = await pg_api_t.test_create_fun()
    return result


@router.get("/test_select/")
async def test_select():
    result = await pg_api_t.test_select_fun()
    return result


@router.get("/test_drop/")
async def test_drop():
    result = await pg_api_t.test_drop_fun()
    return result


@router.get("/test_insert_mongo/")
async def test_insert_mg():
    result = await mg_api_t.test_insert_fun()
    return result


@router.get("/test_select_mongo/")
async def test_select_mg():
    result = await mg_api_t.test_select_fun()
    return result


@router.get("/test_drop_mongo/")
async def test_drop_mg():
    result = await mg_api_t.test_drop_fun()
    return result
