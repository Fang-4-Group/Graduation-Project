import os
import uuid
import httpx

class LineOIDCService:
    def __init__(self):
        self.channel_id = os.getenv('LINE_OIDC_CHANNEL_ID')
        self.channel_secret = os.getenv('LINE_OIDC_CHANNEL_SECRET')
        self.redirect_uri = os.getenv('LINE_OIDC_REDIRECT_URI')
    
    async def generate_auth_url(self):
        state = str(uuid.uuid4()) 
        return (
            f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&"
            f"client_id={self.channel_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"state={state}&scope=profile%20openid"
        )
    
    async def __exchange_code_for_token(self, code: str):
        token_url = "https://api.line.me/oauth2/v2.1/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.channel_id,
            "client_secret": self.channel_secret,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, headers=headers, data=data)
            return response.json()

    async def __get_userinfo(self, access_token: str):
        userinfo_url = "https://api.line.me/v2/profile"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(userinfo_url, headers=headers)
            return response.json()

    async def authorization_callback(self, code):
        token_response = await self.__exchange_code_for_token(code)
        access_token = token_response.get("access_token")
        userinfo = await self.__get_userinfo(access_token)
        line_id = userinfo.get("userId")
        return {"line_id": line_id}
