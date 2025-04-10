from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')

settings = Settings()
