import datetime
import os

from . import default


class Config(default.Config):
    """
        production config
    """
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.environ.get('MYSQL_USER', "groundworx"),
        os.environ.get('MYSQL_PASS', "groundworx"),
        os.environ.get('MYSQL_HOST', "mysql"),
        os.environ.get('MYSQL_DB', "groundworx"),
    )
    APP_HOST = "http://test-bucket-gw.s3-website-us-west-1.amazonaws.com/"
    BUCKET_NAME = 'groundworx-media'
