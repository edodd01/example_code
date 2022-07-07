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
outpath = "/home/emma/S3_copy/"

#S3 session
session = boto3.Session(aws_access_key_id=aws_creds['aws_access_key_id'],
                        aws_secret_access_key=aws_creds['aws_secret_access_key'],
                        region_name="eu-central-1")
s3 = session.resource("s3")
bucket = s3.Bucket(name=bucket_name)
for s3_file in bucket.objects.all():
    path, filename = os.path.split(s3_file.key)
    if not os.path.exists(outpath+path):
        os.makedirs(outpath+path)
    print(outpath+path+'/'+filename)
    bucket.download_file(s3_file.key, outpath+path+'/'+filename)

print("DONE")
