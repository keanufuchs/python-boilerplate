"""Configuration module for DNACrafter."""

import json
import logging.config

from pydantic import ValidationError
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

from app.utils.sheets_builder import get_directory_as_yml_string

with open('app/config/logging.json') as cfgfile:
    config = json.load(cfgfile)
    logging.config.dictConfig(config)

class BaseConfig(BaseSettings):
    """Base configuration class for DNACrafter."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        yaml_file='app/config/config.yml')

    @classmethod
    def settings_customise_sources( # noqa: D102
        cls,
        settings_cls: type[BaseSettings],
        dotenv_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
        init_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),
                env_settings,
                dotenv_settings,)

    # Logging Settings
    VERBOSE: bool = False



try:
    CONFIG = BaseConfig()
except ValidationError as err:
    print(err)
    exit(1)
