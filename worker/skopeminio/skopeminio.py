import boto3
import os
'''
This class was made to interact with MinIO. It uses boto3 to interact with 
the MinIO API. More information for boto3 is found at
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

This is used to reduce the number of custom functions needed for 
certain projects used by our organization.
'''

class Minioconnect():
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key):
        self.client = boto3.client('s3',
            endpoint_url = endpoint_url,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key, 
            verify = False)
        self.resource = boto3.client('s3',
            endpoint_url = endpoint_url,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key, 
            verify = False)
    def insert_file(self, Body, Bucket, Key):
        self.bucket = Bucket
        self.key = Key
        self.body = Body
        self.write_results()
        self.generate_url()
    def write_results(self):
        self.response = self.client.put_object(Body = self.body, Bucket = self.bucket, \
            Key = self.key)
    def generate_url(self):
        self.presigned_url = self.client.generate_presigned_url(
                                ClientMethod='get_object',
                                Params={
                                    'Bucket': self.bucket,
                                    'Key': self.key
                                }
                            )
        self.href_string="<a href="+self.presigned_url+">"+self.key+"</a>"
    def move_file(self, **kwargs):
        copy_source={
            'Bucket': kwargs.get('source_bucket'),
            'Key': kwargs.get('file')
        }
        destination_bucket = self.resource.Bucket(kwargs.get('destination_bucket'))
        destination_bucket.copy(copy_source, copy_source.get('Key'))
        self.resource.Object(kwargs.get('source_bucket')),
        copy_source.get('Key').delete()
    def move_and_rename(self, **kwargs):
        self.client.copy_object(Bucket = kwargs.get('destination_bucket'), \
                                        CopySource = f"{kwargs.get('source_bucket')}/{kwargs.get('old_filename')}", \
                                        Key = kwargs.get('source_bucket'))
        self.client.delete_object(Bucket = kwargs.get('source_bucket'), Key = kwargs.get('old_filename'))