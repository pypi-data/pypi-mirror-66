import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # JWT CONF
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', "039urfjd9sf8usdf9ijdsf;lsdlf23/;el23p")
    SECRET_KEY = os.urandom(24)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=os.environ.get('JWT_EXPIRES', 7))
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.environ.get('MYSQL_USER', "groundworx"),
        os.environ.get('MYSQL_PASS', "groundworx"),
        os.environ.get('MYSQL_HOST', "mysql"),
        os.environ.get('MYSQL_DB', "groundworx"),
    )
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')

    MYSQL_DB = os.environ.get('MYSQL_DB', "db")
    # DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_HOST = "http://test-bucket-gw.s3-website-us-west-1.amazonaws.com/recover-password"
    BUCKET_NAME = 'groundworx-media'

    @staticmethod
    def init_app(app):
        pass