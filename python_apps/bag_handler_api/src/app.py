import logging
import random

# Setup logging with the python module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def request_bag_handler(event: object, context):
    try:
        
        ok_response = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": { "Content-Type": "application/json" },
                "body": "OK. Bag Handlers are on the way!"
        }
        
        error_response = {
                "isBase64Encoded": False,
                "statusCode": 429,
                "headers": { "Content-Type": "application/json" },
                "body": "Too Many Requests"
        }
        
        # Return ok 1/50th of the time. Otherwise return a 429
        random_value = random.randint(1,50)
        if random_value == 1:
            return ok_response
        else:
            return error_response
            
       
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e