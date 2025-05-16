from dotenv import load_dotenv
import os

load_dotenv()  

class Config:
    BASE_URL = os.getenv("BASE_URL")
    API_KEY = os.getenv("API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
    DB_NAME = os.getenv("DB_NAME")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    API_URL = os.getenv("API_URL")
