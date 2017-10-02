import boto3
import botocore
import tarfile
from tarfile import TarInfo
from botocore.client import Config
s3_client = boto3.client('s3')
s3_resource=boto3.resource('s3')
def lambda_handler(event, context):
    bucket =event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    new_bucket='uncompressed-data'
    new_key=key[:-4]
    try:
        s3_client.download_file(bucket, key, '/tmp/file')
        if(tarfile.is_tarfile('/tmp/file')):
           tar = tarfile.open('/tmp/file', "r:gz")
           for TarInfo in tar:
              tar.extract(TarInfo.name, path='/tmp/extract/')
           s3_client.upload_file('/tmp/extract/'+TarInfo.name,new_bucket, new_key)
           tar.close()
    except Exception as e:
        print(e)
        raise e
