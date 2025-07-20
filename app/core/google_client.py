import os
import pickle
from typing import Tuple

from aiogoogle.auth.creds import ClientCreds, UserCreds
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from app.core.config import settings
from app.core.constants import SCOPES

load_dotenv()


def auth() -> Tuple[ClientCreds, UserCreds]:
    info = {
        "installed": {
            "client_id": settings.google_client_id,
            "project_id": settings.google_project_id,
            "auth_uri": settings.google_auth_uri,
            "token_uri": settings.google_token_uri,
            "auth_provider_x509_cert_url": settings.google_auth_provider_x509_cert_url,
            "client_secret": settings.google_client_secret,
            "redirect_uris": [settings.google_redirect_uri],
        }
    }

    client_creds = ClientCreds(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=SCOPES,
        redirect_uri=settings.google_redirect_uri,
    )

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(info, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token_file:
            pickle.dump(creds, token_file)

    user_creds = UserCreds(
        token=creds.token,
        refresh_token=creds.refresh_token,
        token_uri=creds.token_uri,
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        scopes=creds.scopes,
        expiry=creds.expiry.isoformat() if creds.expiry else None,
    )

    return client_creds, user_creds


client_creds, user_creds = auth()


async def get_service():
    async with aiogoogle(
        client_creds=client_creds, user_creds=user_creds
    ) as aiogoogle:
        yield aiogoogle
