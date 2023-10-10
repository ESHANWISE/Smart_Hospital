import secrets

SECRET_KEY = secrets.token_urlsafe(20)
ADMIN_EMAIL="ADMIN@PERSONAL.COM"
SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/smartapp_database"