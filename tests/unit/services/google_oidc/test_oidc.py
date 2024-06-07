import os
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

# Adjust these imports based on your actual application structure
from src.main import app
from src.services.google_oidc.oidc import OIDCService

client = TestClient(app)


def test_oidc_service_initialization():
    with patch.dict(
        os.environ,
        {
            "GOOGLE_CLIENT_ID": "fake-id",
            "GOOGLE_REDIRECT_URI": "http://fake-uri",
        },  # noqa
    ):
        service = OIDCService()
        assert service.client_id == "fake-id"
        assert service.redirect_uri == "http://fake-uri"


def test_get_authorization_url():
    with patch.dict(os.environ, {"GOOGLE_REDIRECT_URI": "http://fake-uri"}):
        with patch(
            "src.services.google_oidc.oidc.Flow.from_client_secrets_file",
            return_value=Mock(
                authorization_url=Mock(return_value="http://mock-auth-url")
            ),
        ):
            service = OIDCService()
            url = service.get_authorization_url()
            assert url == "http://mock-auth-url"


def test_fetch_token():
    with patch(
        "src.services.google_oidc.oidc.Flow.from_client_secrets_file"
    ) as MockFlow:
        instance = MockFlow.return_value
        instance.fetch_token.return_value = {"access_token": "fake_token"}
        service = OIDCService()
        token = service.fetch_token("http://response-from-google")
        assert token == {"access_token": "fake_token"}


def test_verify_id_token():
    with patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "fake-id"}):
        with patch("google.auth.transport.requests.Request"), patch(
            "google.oauth2.id_token.verify_oauth2_token",
            return_value={"sub": "1234567890"},
        ):
            service = OIDCService()
            token_info = service.verify_id_token("fake_token")
            assert token_info == {"sub": "1234567890"}
