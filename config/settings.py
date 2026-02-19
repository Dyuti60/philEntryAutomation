import os
from dotenv import load_dotenv
load_dotenv()
## Setting file will set all the project environment variables
class Settings:
    ENV = os.getenv("ENV","QA")
    BASE_URL = os.getenv("BASE_URL")
    API_BASE_URL = os.getenv("API_BASE_URL")
    BROWSER = os.getenv("BROWSER","chromium")
    HEADLESS = bool(os.getenv("HEADLESS",True))
    TIMEOUT = int(os.getenv("TIMEOUT",6000))
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

settings = Settings()