import os


class Config:
    API_URL = os.getenv("API_URL")


config = Config()
