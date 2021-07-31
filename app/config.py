import os

class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    RESULTS_PER_PAGE = 10