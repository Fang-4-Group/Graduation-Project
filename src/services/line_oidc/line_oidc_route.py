from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.services.line_oidc.line_oidc_service import LineOIDCService

load_dotenv()

line_oidc_router = APIRouter(prefix="/line-oidc")

service = LineOIDCService()


@line_oidc_router.get("/")
async def line_login():
    auth_url = service.generate_auth_url()
    return RedirectResponse(auth_url)


@line_oidc_router.get("/callback")
async def handle_callback(request: Request):
    code = request.query_params.get("code")
    token_response = await service.exchange_code_for_token(code)
    access_token = token_response.get("access_token")
    userinfo = await service.get_user_info(access_token)
    return userinfo
