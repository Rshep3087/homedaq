import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "TBkQgbxqSCBKL-SLNA-Q0w"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
