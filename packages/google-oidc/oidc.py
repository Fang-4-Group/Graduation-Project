import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from jinja2 import Environment, FileSystemLoader
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

# Override environment for development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

load_dotenv()
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

# Set up Jinja2 environment
jinja_env = Environment(loader=FileSystemLoader("templates"))


app = FastAPI()

# Setting up session middleware
app.add_middleware(SessionMiddleware, secret_key="!secret")

router = APIRouter(prefix="/google-oidc")

flow = Flow.from_client_secrets_file(
    "client.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ],
    redirect_uri=redirect_uri,
)


@router.get("/login")
async def login(request: Request):
    authorization_url, state = flow.authorization_url()
    request.session["state"] = state
    return RedirectResponse(authorization_url)


@router.get("/auth")
async def auth(request: Request):
    state = request.session.get("state")
    if not state:
        raise HTTPException(
            status_code=400, detail="State not found in session"
        )  # noqa

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session["access_token"] = credentials.token

    try:
        userinfo = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), client_id
        )
        # use jinja template
        template = jinja_env.get_template("profile.html")
        html_content = template.render(userinfo=userinfo)
        return HTMLResponse(content=html_content)

    except ValueError as e:
        print(f"Invalid token: {e}")
        return HTMLResponse(
            content=f"Error: Invalid token - {e}", status_code=400
        )  # noqa


@router.get("/")
def read_root():
    home_temp = jinja_env.get_template("homepage.html")
    html_content = home_temp.render()
    return HTMLResponse(content=html_content)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("oidc:app", host="0.0.0.0", port=8082, reload=True)
