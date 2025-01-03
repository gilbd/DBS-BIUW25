import os

# Database configurations
DB_USER = os.getenv('DB_USER', 'root')  # Change 'root' to your MySQL username
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')  # Replace with your password
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'dbs')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#SECRET_KEY = 'dev'

# Application configurations
DEBUG = True  # Set to False in production
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')