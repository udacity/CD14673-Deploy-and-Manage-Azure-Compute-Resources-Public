import json
import logging
from datetime import datetime
import random
import boto3
import os
import time

# Setup logging with the python module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sns_topic = os.environ.get('SNS_TOPIC','')
sns_client = boto3.client('sns')

'''
This function emits random SNS messages for flights
allowing our downstream functions to parse events
and make updates to data.
'''
def handler(event: object, context):
    try:
        
        # Run the generator a few times to produce a good
        # amount of data
        for i in range(5):
            # get a random flight number and format it to match our data
            rand_flight_number = random.randint(10,25)
            rand_flight = f'AWS{rand_flight_number:04d}'
            
            message = {
                'flight': rand_flight,
                'timestamp': datetime.now().isoformat(),
            }
            
            logger.info(f"Sending event for {rand_flight}")
            
            sns_client.publish(
                TopicArn=sns_topic,
                Message=json.dumps(message),
                Subject=f"Flight {rand_flight} updated"
            )
            time.sleep(1)

    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e