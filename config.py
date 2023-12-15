from pydantic_settings  import BaseSettings
import cloudinary



class Settings(BaseSettings):
    cloudinary_name:str
    cloudinary_api_key:str
    cloudinary_api_secret:str
    postgres_db:str
    postgres_user:str
    postgres_password:str
    postgres_port:str
    postgres_host:str
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379

    def init_cloudinary(self):
        cloudinary.config(
            cloud_name=self.cloudinary_name,
            api_key=self.cloudinary_api_key,
            api_secret=self.cloudinary_api_secret,
            secure=True,
        )
    class Config:
        extra = "ignore"   
        env_file = ".env"
        extra = "ignore"
        env_file_encoding = "utf-8"


settings = Settings()