from dotenv import load_dotenv , dotenv_values
import os


load_dotenv()


class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USERNAME=os.getenv('DB_USERNAME')
    DB_PASSWORD=os.getenv('DB_PASSWORD')
    DB_USER=os.getenv('DB_USER')
    DB_HOST=os.getenv('DB_HOST')
    SECRET_KEY = os.getenv('SECRET_KEY')