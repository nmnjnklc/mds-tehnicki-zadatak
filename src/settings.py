from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

from pathlib import Path


PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


class DBConfig(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    port: str
    name: str
    auth_plugin: str

    def get_db_uri(self) -> str:
        return (f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
                f"?auth_plugin={self.auth_plugin}")


class Settings(BaseSettings):
    database: DBConfig = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=Path(PROJECT_ROOT, ".env"),
        env_nested_delimiter="__",
        case_sensitive=False
    )
