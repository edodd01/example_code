#Code to upload files from a folder to the S3 bucket I have access to.

#imports
import boto3
from botocore.exceptions import ClientError
import os

#Creds
aws_access_key_id = "addkeyhere"
aws_secret_access_key = "addkeyhere"
aws_creds =  {'aws_access_key_id': aws_access_key_id,
              'aws_secret_access_key': aws_secret_access_key}
bucket_name = "bucketname"

#S3 session
session = boto3.Session(aws_access_key_id=aws_creds['aws_access_key_id'],
                        aws_secret_access_key=aws_creds['aws_secret_access_key'],
                        region_name="eu-central-1")
s3_client = session.client("s3")

#Folder to upload
path = "pathtofolder"

for subdir, dirs, files in os.walk(path):
    for fff in files:
        file_name = os.path.join(subdir, fff)
        object_name = file_name.replace(path,"")
        with open(file_name, 'rb') as data:
            response = s3_client.upload_file(file_name, bucket_name, object_name)

print("DONE")
