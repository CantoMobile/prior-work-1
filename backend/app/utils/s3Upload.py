import boto3
from PIL import Image
import io


ACCESS_KEY_ID = 'AKIAVC2XI5TJZHZ2FBBU'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = "cantonica-favicons-test"

def uploadFile(file, image_name):
    s3 = boto3.client('s3',
        aws_access_key_id= ACCESS_KEY_ID,
        aws_secret_access_key= ACCESS_SECRET_KEY
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