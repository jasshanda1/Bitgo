import boto3
from day_beacon.settings import *
import random

access_key_id = AWS_ACCESS_KEY_ID
secret_access_key = AWS_SECRET_KEY
bucket_name = AWS_BUCKET_NAME


def saveImage(image):
    image_name = "{}_{}".format(random.randint(100000, 999999),image.name)
    s3 = boto3.client("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    acl="public-read"
    url = s3.upload_fileobj(
            image,
            bucket_name,
            image_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": image.content_type
            }
        )
    s3_location = "http://{}.s3.ap-south-1.amazonaws.com/".format(bucket_name)
    return "{}{}".format(s3_location, image_name), image_name