from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: EmailStr = "nW3yG@example.com"
    first_superuser_password: str = "pass"

    type: str = ""
    project_id: str = ""
    private_key_id: str = ""
    private_key: str = ""
    email: str = ""
    client_email: str = ""
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    auth_uri: str = ""
    token_uri: str = ""
    auth_provider_x509_cert_url: str = ""
    client_x509_cert_url: str = ""
    google_redirect_uri: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
