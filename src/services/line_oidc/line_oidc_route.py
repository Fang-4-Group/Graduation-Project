from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from services.line_oidc.line_oidc_service import LineOIDCService

load_dotenv()

router = APIRouter(prefix="/line-oidc")

service = LineOIDCService()


@router.get("/")
async def line_login():
    auth_url = service.generate_auth_url()
    return RedirectResponse(auth_url)
