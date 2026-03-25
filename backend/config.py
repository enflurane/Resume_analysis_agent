import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.API_KEY = os.getenv("API_KEY", "")
        self.BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.MAX_FILE_SIZE = 10 * 1024 * 1024
        self.ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png", ".gif"}

settings = Settings()
