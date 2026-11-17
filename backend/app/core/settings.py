#this file is crated for taking information while stay hidden

from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    PROJECT_NAME : str
    SECRECT_KEY : str
    ENCRYPTION_KEY:str
    S3_ENDPOINT:str
    S3_ACCESS_KEY:str
    S3_REGION:str
    S3_BUCKET:str
    S3_SECRET_KEY:str
    EMAIL_SENDER : str
    EMAIL_PASSWORD:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  
    )

setting = Settings()    