from datetime import datetime, timezone
import json
import logging
from . import model
from pydantic import ValidationError
import boto3
from boto3.dynamodb.conditions import Key
import os
from . import sample_values

# Setup logging with the python module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Setup a DDB Client
# Note: this is a global variable as to not
# waste memory setting this up for every invocation of the handler
dynamodb = boto3.resource('dynamodb')
ddb_table = dynamodb.Table(os.environ.get('DDB_TABLE','project_checked_bags'))

'''


'''
def handler(event: object, context):
    try:
        # Log the event to CloudWatch for diagnostics
        logger.info("Received event: " + json.dumps(event))

        # Parse the SQS Event 
        parsedEvent = model.SNSEvent(**event)
        
        # For each record in the SQS Batch
        for record in parsedEvent.Records:
            
            message_data = json.loads(record.Sns.Message)
            flight_message = model.FlightMessage(**message_data)
            flight_number = flight_message.flight
            
            # log the id for diagnostics
            logger.info(f"Processing flight event for {flight_message.flight} sent at {flight_message.timestamp}")
            
            response = ddb_table.query(
                KeyConditionExpression=Key('flight_number').eq(flight_number)
            )

            bags = response['Items']

            # Paginate through remaining results
            while 'LastEvaluatedKey' in response:
                response = ddb_table.query(
                    KeyConditionExpression=Key('flight_number').eq(flight_number),
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                bags.extend(response['Items'])

            for bag_dict in bags:
                bag = model.Checked_Bag(**bag_dict)
                logger.info(f'Updating bag {bag.id}')
                
                # Assume the flight path is DFW -> ORD -> BOS
                # and update accordingly
                match bag.current_location.code:
                    case "ord":
                        logger.info("Bag ${bag.id} arrived in BOS from ORD")
                        bag.location_history.append(bag.current_location)
                        bag.current_location=sample_values.boston_terminal_b_aboard_aircraft
                        bag.updated=datetime.now(timezone.utc)
                    case "dfw":
                        logger.info("Bag ${bag.id} arrvied in ORD from DFW")
                        bag.location_history.append(bag.current_location)
                        bag.current_location=sample_values.chicago_terminal_1_gate
                        bag.updated=datetime.now(timezone.utc)
                    case _:
                        logger.warning(f"Unexpected bag location: {bag.current_location.code}.")
                
                bag_update_str=bag.model_dump_json()
                bag_update_dict=json.loads(bag_update_str)
                
                # Perform an upsert with put_item
                ddb_table.put_item(Item=bag_update_dict)
                logger.info(f"Update location {bag.current_location.code} flight {bag.flight_number} bag {bag.id}")
                
                
            # prepare the DDB Document and insert
            try:
                pass
            except Exception as e:
                logger.error("Error putting record to DDB: " + str(e))
                raise e
     
    except ValidationError as e:
        logger.error("Unable to deserialize JSON: " + str(e.errors()))
        # raise the exception to allow the lambda function to error
        # important for dead-letter queuing
        raise e
    except Exception as e:
        logger.error("An unexpected error has occured: " + str(e))
        # raise the exception to allow the lambda function to error
        # important for dead-letter queuing
        raise e
    