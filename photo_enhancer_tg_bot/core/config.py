from pydantic_settings import BaseSettings


class AwsConfig(BaseSettings):
    endpoint: str
    access_key_id: str
    secret_access_key: str


class LoggerConfig(BaseSettings):
    level: str
    alert_channel: int
    remote_token: str
    file: str = ""


class BotConfig(BaseSettings):
    token: str
    aws: AwsConfig
    logger: LoggerConfig

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


bot_config = BotConfig()
