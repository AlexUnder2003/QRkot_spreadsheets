import os
import pickle
from typing import Tuple

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ClientCreds, UserCreds
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from app.core.config import settings
from app.core.constants import SCOPES

load_dotenv()

INFO = {
    "type": settings.type,
    "project_id": settings.project_id,
    "private_key_id": settings.private_key_id,
    "private_key": settings.private_key,
    "client_email": settings.client_email,
    "client_id": settings.client_id,
    "auth_uri": settings.auth_uri,
    "token_uri": settings.token_uri,
    "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url,
    "client_x509_cert_url": settings.client_x509_cert_url,
}


def auth() -> Tuple[ClientCreds, UserCreds]:
    client_creds = ClientCreds(
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        scopes=SCOPES,
        redirect_uri=settings.redirect_uri,
    )

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token_file:
            pickle.dump(creds, token_file)

    user_creds = UserCreds(
        access_token=creds.token,
        refresh_token=creds.refresh_token,
        scopes=creds.scopes,
        token_uri=creds.token_uri,
        expires_at=creds.expiry,  # datetime or None
    )

    return client_creds, user_creds


client_creds, user_creds = auth()


async def get_service():
    async with Aiogoogle(
        client_creds=client_creds, user_creds=user_creds
    ) as wrapper_service:
        yield wrapper_service
