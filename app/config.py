import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    def __init__(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

settings = Settings() 