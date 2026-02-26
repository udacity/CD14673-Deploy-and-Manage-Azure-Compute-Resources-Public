import json
import logging
import uuid


def lambda_handler(event, context):
    try:
        logging.info("Received event")
        
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
        
        
    except Exception as e:
        error_id = str(uuid.uuid4())
        logging.debug(f"Generated error ID: {error_id}for error: {str(e)}")
        logging.error(f"Error ID: {error_id}")
        
        return {
            'statusCode': 500,
            'body': json.dumps(f"An unexpected error occurred. code: {error_id}")
        }