import boto3
from app.core.settings import setting
from botocore.exceptions import ClientError
bucket_name = setting.S3_BUCKET
s3_clint = boto3.client(
    service_name="s3",
    region_name=setting.S3_REGION,
    aws_access_key_id=setting.S3_ACCESS_KEY,
    aws_secret_access_key=setting.S3_SECRET_KEY,
    endpoint_url=setting.S3_ENDPOINT

)

def bucket_create():
   try:
      s3_clint.head_bucket(Bucket=bucket_name)
      return True
   except ClientError as e :
    error_code = e.response["Error"]["Code"]
    if error_code == "404":
     create_s3_bucket = s3_clint.create_bucket(
        Bucket=setting.S3_BUCKET)
   
     return create_s3_bucket
    else:
      raise e 
  


def save_bytes(Key,data):
   upload=s3_clint.put_object(
        Bucket=bucket_name,
        Key=Key,
        Body=data
    )
   return upload

def read_bytes(Key):
   responce =s3_clint.get_object(Bucket=bucket_name , Key=Key)
   content =responce["Body"].read()
   return content

def delete_bytes(Key):
  responce = s3_clint.delete_object(Bucket=bucket_name , Key = Key)
  return responce