from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname : str 
    database_port : str 
    database_password: str
    database_name : str
    database_username : str 
    secret_key: str 
    algorithm: str 
    acces_token_expire_minutes: int 

    #we use pydantic to collect the necesary data from .env file 
    #for our schema and validated it 
    class Config:
        env_file = ".env"

settings = Settings()

#print(settings.database_username)
