from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Chemin absolu vers le fichier .env, calculé depuis ce fichier config.py
# Structure : EduPilot/edupilot-api/app/config.py
#   parents[0] = app/
#   parents[1] = edupilot-api/
#   parents[2] = EduPilot/
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / "infra" / "db" / ".env"

class Settings(BaseSettings):
    APP_NAME: str = "EduPilot API"
    APP_ENV: str = "development"

    POSTGRES_USER: str = "edupilot"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "edupilot"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
