import os
import boto3
from authentication import admin_validator
from flask_restful import Resource,request
from time import time_ns
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region = os.environ.get('AWS_REGION')
bucket_name = os.environ.get('AWS_BUCKET_NAME')

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=access_key, region_name=region)


class Upload(Resource):
    @admin_validator()
    def post(self):
        file = request.files['file']
        file_name = str(time_ns()) + '.jpg'
        s3.upload_fileobj(file, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'})
        url = 'https://%s.s3.%s.amazonaws.com/%s' % (bucket_name, region, file_name)
        return {'data': url}, 200
