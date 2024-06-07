import os
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow


class OIDCService:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

        self.flow = Flow.from_client_secrets_file(
            "src/services/google_oidc/client.json",
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid",
            ],
            redirect_uri=self.redirect_uri,
        )

    # Solving disallowed user agent error
    def append_open_external_browser_param(url: str) -> str:
        url_parts = list(urlparse(url))
        query = parse_qs(url_parts[4])
        query["openExternalBrowser"] = ["1"]
        url_parts[4] = urlencode(query, doseq=True)
        return urlunparse(url_parts)

    def get_authorization_url(self):
        auth_url = self.flow.authorization_url()
        auth_url_with_param = self.append_open_external_browser_param(auth_url)
        return auth_url_with_param

    def fetch_token(self, authorization_response):
        return self.flow.fetch_token(
            authorization_response=authorization_response
        )  # noqa

    def verify_id_token(self, token):
        return id_token.verify_oauth2_token(
            token, requests.Request(), self.client_id, clock_skew_in_seconds=60
        )
