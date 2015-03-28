import os

class DevelopmentConfig(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("IG_SECRET_KEY", "")