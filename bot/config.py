import os

from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных из.env

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
HOST = os.getenv("HOST")
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
PORT = os.getenv("PORT")
