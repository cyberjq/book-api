import typing
from pydantic import BaseSettings, Field, BaseModel


class AppConfig(BaseModel):
    """Application configurations."""
    debug: typing.Optional[bool] = False


class GlobalConfig(BaseSettings):
    """Global configurations."""

    ENV_STATE: typing.Optional[str] = Field(None, env="ENV_STATE")
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@postgresserver/db_model"

    # application config
    APP_CONFIG: AppConfig = AppConfig()

    def __init__(self, **values: typing.Any):
        super().__init__(**values)

        if self.ENV_STATE == "dev":
            self.APP_CONFIG = AppConfig(debug=True)

    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    USER_POSTGRES_DEV: typing.Optional[str] = Field(None, env="USER_POSTGRES_DEV")
    PASSWORD_POSTGRES_DEV: typing.Optional[str] = Field(None, env="PASSWORD_POSTGRES_DEV")
    HOST_POSTGRES_DEV: typing.Optional[str] = Field(None, env="HOST_POSTGRES_DEV")
    PORT_POSTGRES_DEV: typing.Optional[int] = Field(None, env="PORT_POSTGRES_DEV")
    DATABASE_POSTGRES_DEV: typing.Optional[str] = Field(None, env="DATABASE_POSTGRES_DEV")

    def __init__(self, **values: typing.Any):
        super().__init__(**values)
        self.SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" \
                                  f"{self.USER_POSTGRES_DEV}:" \
                                  f"{self.PASSWORD_POSTGRES_DEV}@" \
                                  f"{self.HOST_POSTGRES_DEV}:{self.PORT_POSTGRES_DEV}/" \
                                  f"{self.DATABASE_POSTGRES_DEV}"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    USER_POSTGRES_PROD: typing.Optional[str] = Field(None, env="USER_POSTGRES_PROD")
    PASSWORD_POSTGRES_PROD: typing.Optional[str] = Field(None, env="PASSWORD_POSTGRES_PROD")
    HOST_POSTGRES_PROD: typing.Optional[str] = Field(None, env="HOST_POSTGRES_PROD")
    PORT_POSTGRES_PROD: typing.Optional[int] = Field(None, env="PORT_POSTGRES_PROD")
    DATABASE_POSTGRES_PROD: typing.Optional[str] = Field(None, env="DATABASE_POSTGRES_PROD")

    def __init__(self, **values: typing.Any):
        super().__init__(**values)
        self.SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" \
                                       f"{self.USER_POSTGRES_PROD}:" \
                                       f"{self.PASSWORD_POSTGRES_PROD}@" \
                                       f"{self.HOST_POSTGRES_PROD}:{self.PORT_POSTGRES_PROD}/" \
                                       f"{self.DATABASE_POSTGRES_PROD}"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: typing.Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()
