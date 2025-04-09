from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import HttpUrl, PostgresDsn, SecretStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Fetch the prefix from the environment or set a default
environment_prefix: str = os.getenv("ENVIRONMENT", "DEV_")

BASE_DIR: Path = Path(__file__).absolute().parent.parent.parent


class EnvBaseSettings(BaseSettings):
    environment: str = environment_prefix
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class LoggingConfig(EnvBaseSettings):
    log_level: str = "INFO"
    file: Optional[str] = None
    serializer: bool = False
    alert_channel: int
    remote_token: SecretStr

    class Config:
        env_prefix: str = f"{environment_prefix}_LOG_"


class BotSettings(EnvBaseSettings):
    token: SecretStr
    alerts_chanel: str
    admin_token: str
    chat_id: str
    model_config = SettingsConfigDict(env_prefix=f"{environment_prefix}_BOT_")


class CacheSettings(EnvBaseSettings):
    host: str = "redis"
    port: int = 6379
    ttl: str = ""
    db: str = "0"
    password: Optional[str] = None

    @property
    def redis_url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

    class Config:
        env_prefix = "REDIS_"


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    base_dir: Path = BASE_DIR
    logger: LoggingConfig = LoggingConfig()
    # sentry: SentryConfig = SentryConfig()
    # gitlab: GitlabConfig = GitlabConfig()
    # aws: AWSConfig = AWSConfig()
    cache: CacheSettings = CacheSettings()
    # image_process: ImageProcessAPI = ImageProcessAPI()
    # database: DatabaseConfig = DatabaseConfig()


bot_config = Settings()
