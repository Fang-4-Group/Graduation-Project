import os

from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow


class OIDCService:
    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        client_secrect_file = os.getenv("GOOGLE_SECRECT_FILE")

        self.flow = Flow.from_client_secrets_file(
            client_secrect_file,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid",
            ],
            redirect_uri=self.redirect_uri,
        )

    def get_authorization_url(self):
        return self.flow.authorization_url()

    def fetch_token(self, authorization_response):
        return self.flow.fetch_token(
            authorization_response=authorization_response
        )  # noqa

    def verify_id_token(self, token):
        return id_token.verify_oauth2_token(
            token, requests.Request(), self.client_id, clock_skew_in_seconds=60
        )
