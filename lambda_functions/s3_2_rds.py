import json
import urllib
import boto3
import jaydebeapi

print('Loading function')

s3 = boto3.client('s3')
cf = boto3.client('cloudformation')
tests3 = boto3.resource(u's3')

def _get_stack_outputs(stack):
    for item in cf.describe_stacks(StackName=stack)['Stacks'][0]['Outputs']:
        if item['OutputKey'] == 'JDBCAuroraConnectionString':
            return item['OutputValue']

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
        bucket = tests3.Bucket(u'bg-glue')
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
