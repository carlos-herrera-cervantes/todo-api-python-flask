from mongoengine import connect

from settings import MONGODB_DATABASE

class Config:

    @staticmethod
    def start_connection():
        connect(MONGODB_DATABASE)