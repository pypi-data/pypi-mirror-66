import hashlib
import os
import time

import boto3 as boto3
from werkzeug.utils import secure_filename

from gwlib.config import config
from gwlib.base.base_service import BaseService


class BaseUploadService(BaseService):

    def __init__(self):
        super().__init__()

    def upload(self, file):
        environment = os.getenv('FLASK_ENV')
        environment = config.get(environment)
        host = "https://{}.s3.amazonaws.com".format(environment.BUCKET_NAME)
        filename = file.filename
        filename_splited = filename.split(".")
        if len(filename_splited) <= 1:
            raise Exception("MALFORMED filename")

        extension = filename_splited[-1]
        mimetype = file.content_type
        filename = hashlib.sha256(str(secure_filename(file.filename) +
                                      str(time.time())).encode('utf-8')).hexdigest() + ".{}".format(extension)
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv('AWS_UPLOAD_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_UPLOAD_SECRET')
        )
        s3.put_object(Key=filename, ACL='public-read',
                      ContentType=mimetype,
                      Bucket=environment.BUCKET_NAME, Body=file.stream.read())
        file_url = "{}/{}".format(host, filename)
        return {'success': True,
                "file_url": file_url,
                "file_name": filename
                }


