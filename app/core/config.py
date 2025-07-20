from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: EmailStr = "nW3yG@example.com"
    first_superuser_password: str = "pass"

    google_client_id: str
    google_project_id: str
    google_auth_uri: str
    google_token_uri: str
    google_auth_provider_x509_cert_url: str
    google_client_secret: str
    google_redirect_uri: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
