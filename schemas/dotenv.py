from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSetting(BaseSettings):
    
    host: str
    port: int
    name: str
    user: str
    password: str


    model_config = SettingsConfigDict(env_file='.env',
     env_prefix="DB_", 
     extra='ignore') 


class Settings(BaseSettings):
    db: DbSetting = DbSetting()

    model_config =  SettingsConfigDict(env_file='.env',
     extra='ignore')


settings = Settings()