import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DDB_TABLE', 'project_checked_bags'))

def handler(event, context):
    for record in event['Records']:
        try:
            # SQS body is a JSON string — parse it
            body = json.loads(record['body'])

            current_location = body.get('current_location')
            if not isinstance(current_location, dict) or not isinstance(current_location.get('code'), str):
                raise ValueError("Invalid bag item: current_location.code must be a string")

            # Write to DynamoDB — preserve nested structure exactly
            table.put_item(Item=body)

            print(f"Successfully processed bag: {body.get('id', 'unknown')}")

        except Exception as e:
            # re-raise so Lambda marks the record as failed and SQS routes it to the DLQ
            print(f"Error processing record: {e}")
            raise
