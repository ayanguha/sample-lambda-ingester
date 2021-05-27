import json
import urllib3
import os
import boto3
from datetime import datetime
from io import BytesIO

def set_all_clients():
    s3_client = boto3.client('s3')
    secretsmanager_client = boto3.client('secretsmanager')
    return (s3_client, secretsmanager_client)

def get_fn():
    ## Return File Name
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_api_key(client, key_name):
    response = client.get_secret_value(SecretId=key_name)
    token = json.loads(response['SecretString'])['API_KEY']
    return token

def extract_data(uri, token, fields):
    pm = urllib3.PoolManager()
    headers = {"X-Api-Key": token}
    if fields:
        fields = json.loads(fields)
        resp = pm.request('GET', uri, headers=headers, fields=fields)
    else:
        resp = pm.request('GET', uri, headers=headers)
    resp_json = resp.data
    return BytesIO(resp_json)

def sample_ingester(event, context):
    ## Get S3 and ASM Client
    s3c,smc = set_all_clients()

    ## Read API URI
    uri = os.environ['API_URI']

    ## Get API Key from AWS Secrets Manager
    token = get_api_key(smc, os.environ['API_KEY_NAME'])
    ## Params is optional. Try to read it.
    try:
        fields = os.environ['PARAMS']
    except:
        fields = None

    ## Extract Data from API. It is wrapped in BytesIO as a file like object
    data = extract_data(uri, token, fields)

    ## Come up with a file name. Possibly use UUID or any other mechanism.
    filename = get_fn() + os.environ['SUFFIX']
    key = os.path.join(os.environ['PREFIX'], filename)

    ## Finally, Write to the file
    try:
        s3c.upload_fileobj(Fileobj = data, Bucket=os.environ['BUCKET_NAME'], Key=key)
    except:
        raise
    ## To Do
    ## Logging
    return "Success"
