import base64
from io import BytesIO
import uuid
import logging
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET


class BotoService:
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    @staticmethod
    async def upload_image(base64_image):
        try:
            base64_image = base64_image.split(',')[1]
            image_data = base64.b64decode(base64_image)
        except:
            raise HTTPException(status_code=401, detail='Base64 image error')
        unique_filename = str(uuid.uuid4()) + '.jpg'

        file_path = f'images/{unique_filename}'
        with BytesIO(image_data) as image_stream:
            s3_client = boto3.client('s3')
            try:
                s3_client.upload_fileobj(image_stream, BUCKET, file_path)
                s3_client.put_object_acl(
                    ACL='public-read',
                    Bucket=BUCKET,
                    Key=file_path
                )
                s3_url = f"https://{'my-crypto-wallet'}.s3.{'us-east-1'}.amazonaws.com/{file_path}"
                return s3_url
            except ClientError as e:
                logging.error(e)
                return False



