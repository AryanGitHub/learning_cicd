from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings (BaseSettings):
    
    ENVIRONMENT : str
    db_protocol : str = "postgresql://"
    db_hostname : str = "localhost"
    db_port : int = 5432
    db_username : str = "postgres"
    db_password : str
    db_name : str = "cs_explorer_db"
    #postgres_connection_url : PostgresDsn = db_protocol+db_hostname+ ":" + db_password + "@" + db_hostname + ":" + db_port + "/" + db_name
    secret : str 
    token_timeout_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()
