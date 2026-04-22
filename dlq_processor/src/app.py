import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DLQ_TABLE', 'project_dead_letters'))

def handler(event, context):
    for record in event['Records']:
        try:
            # Store the failed message in long-term storage
            item = {
                'message_id': record['messageId'],
                'body': record['body'],
                'stored_at': datetime.utcnow().isoformat(),
                'source_queue': 'Project_Bag_Check_Queue',
                'error_reason': 'Failed processing after max retries'
            }

            table.put_item(Item=item)

            print(f"Stored DLQ message: {record['messageId']}")

        except Exception as e:
            print(f"Error storing DLQ message: {e}")
            raise
