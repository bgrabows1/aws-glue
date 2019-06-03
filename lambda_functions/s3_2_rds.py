import json
import urllib
import boto3
import jaydebeapi
from botocore.exceptions import ClientError

print('Loading function')

s3 = boto3.client('s3')
cf = boto3.client('cloudformation')
s3 = boto3.resource(u's3')
session = boto3.session.Session()

def get_secret(session, secret_name, region_name):

    if session:
        # Create a Secrets Manager client
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    else:
        raise Exception('Session points to null value.')

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

def get_stack_outputs(stack, output):
    for item in cf.describe_stacks(StackName=stack)['Stacks'][0]['Outputs']:
        if item['OutputKey'] == output:
            print(item['OutputValue'])

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    copy_source = {'Bucket':source_bucket , 'Key':key}
    print(event)

    #just print function
    print("Log stream name : ", context.log_stream_name)
    print("Log group name : ", context.log_group_name)
    print("Request Id:", context.aws_request_id)
    print("Mem. limit(MB): ", context.memory_limit_in_mb)

    try:
        print("Using waiter to waiting for object to persist thru s3 service")
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=key)
        print("Accessing the receied file and reading the same")
        bucket = s3.Bucket(u'bg-glue')
        obj = bucket.Object(key='aurora/homes.csv')
        response = obj.get()
        print("response from file object")
        print(response)
        lines = response['Body'].read().split()
        print(response['Body'].read())

        # creating a list of dictionaries from the csv file records
        recList = list()
        i = 0
        while i < len(lines):
            record  = {}
            record['Sell']      = lines[i]
            record['List']      = lines[i+1]
            record['Living']    = lines[i+2]
            record['Rooms']     = lines[i+3]
            record['Beds']      = lines[i+4]
            record['Baths']     = lines[i+5]
            record['Age']       = lines[i+6]
            record['Acres']     = lines[i+7]
            record['Taxes']     = lines[i+8]
            print(record)
            recList.append(record)
            i = i+9
        println(recList)

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, source_bucket))
