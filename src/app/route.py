from fastapi import APIRouter

from database.seeds import pg_api_for_testing as pg_api_t

router = APIRouter()


@router.get("/test_create/")
async def test_create():
    result = await pg_api_t.test_create_fun()
    if result is None:
        content = {"message": "database not connected"}
    else:
        content = {"message": "success to create table"}
    return content


@router.get("/test_select/")
async def test_select():
    result = await pg_api_t.test_select_fun()
    if result is None:
        content = {"message": "database not connected"}
    else:
        content = {"message": "success to access data", "result": result}
    return content


@router.get("/test_drop/")
async def test_drop():
    result = await pg_api_t.test_drop_fun()
    if result is None:
        content = {"message": "database not connected"}
    else:
        content = {"message": "success to drop table"}
    return content
