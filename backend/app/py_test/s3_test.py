from app.core.settings import setting
import boto3
from app.file_storage_cloud.s3_storage import bucket_create , read_bytes ,save_bytes  ,delete_bytes
bucket_create()
# save_bytes("text/text.txt" , b"hallo")
responce = read_bytes("2/88b42d36b4a344ae9adc3de9baa2a97b.pptx.enc")
print(len(responce))

# responce = delete_bytes("2/c40abf96f7da4b1bb4f8b9ce42739dea.pptx.enc")
# print(len(responce))














# s3_clint = boto3.client(
#     service_name="s3",
#     region_name=setting.S3_REGION,
#     aws_access_key_id=setting.S3_ACCESS_KEY,
#     aws_secret_access_key=setting.S3_SECRET_KEY,
#     endpoint_url=setting.S3_ENDPOINT
# )
# responce = s3_clint.create_bucket(
#     Bucket=setting.S3_BUCKET,
   
# )
# bucket_name = setting.S3_BUCKET

# responce_2 = s3_clint.list_buckets()
# for buckets in responce_2["Buckets"]:
#     print(buckets["Name"])

# data_bytes  =b"hallo"

# upload = s3_clint.put_object(
#     Bucket=bucket_name,
#     Key="test/other.txt",
#     Body=data_bytes
# )
# responce_3 = s3_clint.get_object(Bucket=bucket_name,Key="test/other.txt")
# content = responce_3["Body"].read()
# print(content)


