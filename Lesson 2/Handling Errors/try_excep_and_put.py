import json
import logging
import boto3

error_table = boto3.resource('dynamodb').Table('error_table')

def lambda_handler(event, context):
    try:
        logging.info("Received event")
        
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
        
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        error_table.put_item(Item={
            'id': context.aws_request_id,
            'error_message': str(e),
            'event': json.dumps(event)
        })
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }