import boto3
from PIL import Image
import io
import os
from app.utils.logger import logger


ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
ACCESS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')


def uploadFile(file, image_name):
    logger.info('Uploading files to AWS')
    logger.info(" ACCESS ID " + ACCESS_KEY_ID + " KEY " + ACCESS_SECRET_KEY + " BUCKET " + BUCKET_NAME)
    s3 = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY
    )

    bucket_name = BUCKET_NAME
    with io.BytesIO(file) as file_stream:
        response = s3.upload_fileobj(
            file_stream,
            bucket_name,
            image_name
        )
    public_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_name}"
    return public_url

