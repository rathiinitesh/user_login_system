import os


class Config:
    SECRET_KEY = '0f83efa6ca0046f107b1235989a3597a'
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')