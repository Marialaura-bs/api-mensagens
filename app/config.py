import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'messages.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY='theoelaurabests'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15) # Access tokens expire after 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) # Refresh tokens expire after 30 days