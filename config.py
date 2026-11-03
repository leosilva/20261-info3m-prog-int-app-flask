import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta')
    SUAP_URL = os.getenv('SUAP_URL', 'https://suap.ifrn.edu.br')
    SUAP_CLIENT_ID = os.getenv('SUAP_CLIENT_ID')
    SUAP_CLIENT_SECRET = os.getenv('SUAP_CLIENT_SECRET')
    DB_PASSWORD = os.getenv("DB_PASSWORD", "labinfo") 
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_NAME = "2026-info3m"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@localhost:3306/{DB_NAME}"
