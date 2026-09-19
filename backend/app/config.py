from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str="OMNICRYPTO"
    api_prefix:str="/api"
    risk_free_rate:float=0.0
    data_period:str="5y"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
