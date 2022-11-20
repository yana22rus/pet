import os


class Config(object):
    DEBUG = True

    SECRET_KEY = "1231231231"

    JWT_SECRET_KEY = "qqq12313"

    JWT_TOKEN_LOCATION = ['cookies']

    DATABASE_URI = "/home/qwe/pet.sqlite"

    UPLOAD_FOLDER = os.path.join("img", "uploads")

    MAX_CONTENT_LENGTH = 16 * 1042 * 1042
