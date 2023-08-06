import datetime

from . import default


class Config(default.Config):
    """
        development config
    """
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:groundworx$20@gwdb.cdwxp72nniac.us-east-1.rds.amazonaws.com" \
                              "/groundworx".format(
    )
    APP_HOST = "http://test-bucket-gw.s3-website-us-west-1.amazonaws.com/recover-password"
    BUCKET_NAME = 'groundworx-media'

