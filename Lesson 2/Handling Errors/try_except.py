import json
import logging



def lambda_handler(event, context):
    try:
        logging.info("Received event")
        
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
        
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }