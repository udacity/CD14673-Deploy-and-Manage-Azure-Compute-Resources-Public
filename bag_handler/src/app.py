import json
import time
import random
import urllib3
import boto3
import os

http = urllib3.PoolManager()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DDB_TABLE', 'project_checked_bags'))

BAG_HANDLER_URL = os.environ.get('BAG_HANDLER_URL', '')


def call_with_backoff(url, max_retries=15):
    for attempt in range(max_retries):
        response = http.request('POST', url)
        if response.status == 200:
            return response
        if response.status == 429:
            wait = min((2 ** attempt) + random.uniform(0, 1), 10)
            print(f"Got 429, retrying in {wait:.1f}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
    raise Exception(f"Bag Handler API failed after {max_retries} retries")


def update_bags_at_bos():
    response = table.scan(
        FilterExpression='current_location.code = :loc',
        ExpressionAttributeValues={':loc': 'bos'}
    )

    updated = 0
    for item in response['Items']:
        table.update_item(
            Key={'flight_number': item['flight_number'], 'id': item['id']},
            UpdateExpression='SET checked_in = :ci, claimed = :cl',
            ExpressionAttributeValues={
                ':ci': False,
                ':cl': True
            }
        )
        updated += 1

    return updated


def handler(event, context):
    handler_url = BAG_HANDLER_URL.rstrip('/') + '/handler'

    try:
        call_with_backoff(handler_url)
        print("Bag Handler API call succeeded")
    except Exception as e:
        print(f"Bag Handler API error: {e}")
        raise

    updated = update_bags_at_bos()
    print(f"Updated {updated} bags at BOS: checked_in=False, claimed=true")

    return {'statusCode': 200, 'body': json.dumps({'updated': updated})}
