from .exp import DynamoExporter
from .imp import DynamoImporter

import boto3
from botocore.exceptions import ClientError

def ddb_exists(table_name, region='eu-central-1'):
    try:
        boto3.client('dynamodb', region_name=region).describe_table(TableName=table_name)

        return True

    except ClientError as ce:

        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        else:
            raise ce