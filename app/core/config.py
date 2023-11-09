from typing import Literal, Optional

from pydantic import BaseModel, BaseSettings, parse_file_as, validator


class Mapping(BaseModel):
    enabled: bool | str = True
    method: Literal["POST", "GET", "DELETE", "PUT"] | None = None
    url: str | None = None
    body: dict[str, str] | str | None = None
    headers: dict[str, str] | str | None = None
    query: dict[str, str] | str | None = None


class ControlThePayloadConfig(BaseModel):
    mapping: Mapping


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"

    STREAMER_NAME: str

    PORT_ORG_ID: str
    GITLAB_URL: str = "https://gitlab.com/"
    KAFKA_CONSUMER_BROKERS: str = "localhost:9092"
    KAFKA_CONSUMER_SECURITY_PROTOCOL: str = "plaintext"
    KAFKA_CONSUMER_AUTHENTICATION_MECHANISM: str = "none"
    KAFKA_CONSUMER_USERNAME: str = "local"
    KAFKA_CONSUMER_PASSWORD: str = ""
    KAFKA_CONSUMER_SESSION_TIMEOUT_MS: int = 45000
    KAFKA_CONSUMER_AUTO_OFFSET_RESET: str = "earliest"
    KAFKA_CONSUMER_GROUP_ID: str = ""

    KAFKA_RUNS_TOPIC: str = ""

    CONTROL_THE_PAYLOAD_CONFIG_PATH: str | None = None

    @validator("KAFKA_RUNS_TOPIC", always=True)
    def set_kafka_runs_topic(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str) and v:
            return v
        return f"{values.get('PORT_ORG_ID')}.runs"

    KAFKA_CHANGE_LOG_TOPIC: str = ""

    @validator("KAFKA_CHANGE_LOG_TOPIC", always=True)
    def set_kafka_change_log_topic(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str) and v:
            return v
        return f"{values.get('PORT_ORG_ID')}.change.log"

    class Config:
        case_sensitive = True

    WEBHOOK_INVOKER_TIMEOUT: int = 5
    GITLAB_PIPELINE_INVOKER_TIMEOUT: int = 5


settings = Settings()


def load_control_the_payload_config() -> list[ControlThePayloadConfig] | None:
    control_the_payload_config: None | list[ControlThePayloadConfig] = None
    if mapping_path := settings.CONTROL_THE_PAYLOAD_CONFIG_PATH:
        control_the_payload_config = parse_file_as(
            list[ControlThePayloadConfig], mapping_path
        )

    return control_the_payload_config
