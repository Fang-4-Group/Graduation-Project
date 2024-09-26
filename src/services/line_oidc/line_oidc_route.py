from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from services.line_oidc.line_oidc_service import LineOIDCService

load_dotenv()

router = APIRouter(prefix="/line-oidc")

service = LineOIDCService()


@router.get("/")
async def line_login():
    auth_url = service.generate_auth_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
async def handle_callback(request: Request):
    code = request.query_params.get("code")
    token_response = await service.exchange_code_for_token(code)
    access_token = token_response.get("access_token")
    userinfo = await service.get_user_info(access_token)
    return userinfo
