import os

class Config:
    SECRET_KEY = "chatverse_secret_key"

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:soumi_2772@localhost:5432/chatverse_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False