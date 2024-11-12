import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    CALLBACK_URL = os.getenv("CALLBACK_URL")
