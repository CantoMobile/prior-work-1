import boto3
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
ACCESS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

def uploadFile(file, image_name):
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