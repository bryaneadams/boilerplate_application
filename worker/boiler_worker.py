from redis import Redis
from rq import Queue, Worker, Connection
import os
import json
from datetime import datetime
from skopeminio import Minioconnect

'''
Connecto to Redis queue
'''

redis = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT')
)

workers = Worker.all(connection=redis)
queue = [os.getenv('REDIS_QUEUE')]

'''
Connect to MinIO
'''

s3 = Minioconnect(
    endpoint_url = f"http://{os.getenv('MINIO_ENDPOINT')}",
    aws_access_key_id = os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key = os.getenv('MINIO_SECRET_KEY'), 
)

bucket = os.getenv('MINIO_DEFAULT_BUCKETS')

def run_job(payload):
    
    '''
    In this example I write the statment to a text file in MinIO
    In this example I generate a file anem with date time in order
    prevent keys from being repeated (although there is a non-zero 
    probability of repated names...It is just really small)
    '''

    filename = f"{datetime.now().strftime('%d-%m-%Y_%H:%M:%S')}_Bryan_Rocks.txt"

    s3.insert_file(Body=payload['statement'], Bucket=bucket, Key=filename)


if __name__ == "__main__":
    with Connection(redis):
        w = Worker(queue)
        w.work()
