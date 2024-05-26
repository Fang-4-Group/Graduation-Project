from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from starlette.responses import RedirectResponse

from database.migrations.mongodb_init import MongoDBInitClient
from database.migrations.pg_CRUD import PosgresqClient
from database.migrations.posgresql_init import PosgresqlInitClient
from database.seeds.mongo_api_for_testing import MongoDBClient
from database.seeds.pg_api_for_testing import PosgresqTestClient

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
