from dotenv import load_dotenv
import os

load_dotenv(override=True)

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_PREFIX = os.environ.get('DB_PREFIX', '')