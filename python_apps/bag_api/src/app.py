from datetime import datetime, timezone
import json
import logging
import os
import boto3
from . import model
from boto3.dynamodb.conditions import Key, Attr

from pydantic import ValidationError
from itertools import groupby
import urllib


# Setup logging with the python module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Setup a DDB Client
# Note: this is a global variable as to not
# waste memory setting this up for every invocation of the handler
dynamodb = boto3.resource('dynamodb')
ddb_table = dynamodb.Table(os.environ.get('DDB_TABLE','project_checked_bags'))


'''
Scan and return the DDB data as a JSON string
'''
def get_all_documents():
    filter = Attr('flight_number').ne('unknown') # filter out DLQ
    response = ddb_table.scan(FilterExpression=filter)
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = ddb_table.scan(FilterExpression=filter, ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return json.dumps(data)


''' 
Calculate the time customers spend waiting at the destination
for the dashboard view
'''
def get_wait_time_handler(event: object, context):
    try:
        
        data= get_all_documents()
        json_data = json.loads(data)
        now = datetime.now(timezone.utc)
        
        #get minutes from last updated value using comprehension
        bos_rows = [((now-datetime.fromisoformat(x['updated'])).total_seconds()/60) for x in json_data if x['current_location']['code']=='bos']
       
        #build the avg time
        bos_sum = sum(bos_rows)
        cnt = len(list(bos_rows))
        avg = bos_sum /cnt
        avg = round(avg,2)
        
    
        result = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": { 
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                    },
                "body": str(avg)
        }
        return result 
        
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e
    

'''
Call get_all_documents and summarize the data by Location and Flight for the
dashboard application view.
'''
def dashboard_handler(event: object, context):
    try:
        
        data= get_all_documents()
        json_data = json.loads(data)
        json_data = [x for x in json_data if x['checked_in']==True]
        summaries={}
        
        for key, group in groupby(json_data, lambda x: x['current_location']['code'] ):
            for x in group:
                if key in summaries:
                    summaries[key] = summaries[key]+1
                else:
                    summaries[key]=0

        print("Summaries")
        result = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin":"*"},
                "body": json.dumps(summaries)
        }
        return result 
        
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e
    

'''
Call get_all_documents and format the result for API Gateway Proxy Integration
'''
def get_bags_handler(event: object, context):
    try:
            
        result = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": { "Content-Type": "application/json","Access-Control-Allow-Origin":"*" },
                "body": get_all_documents()
        }
        return result 
        
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e
    

'''
Get a specfic bag document and format the result for API Gateway Proxy Integration
'''
def get_bag_handler(event: object, context):
    try:
        logger.info("Received event: "+ json.dumps(event))
        event_data = model.APIGWEvent(**event)
        flight_number = urllib.parse.unquote(event_data.pathParameters.flight_number)
        bag_id = urllib.parse.unquote(event_data.pathParameters.bag_id) if event_data.pathParameters.bag_id is not None else None
        logger.info(f"Getting bag {bag_id} from flight {flight_number}")
  
        response = ddb_table.query(
            KeyConditionExpression=Key('flight_number').eq(flight_number) & Key('id').eq(bag_id)  
        )

        bags = response['Items']
        # Paginate through remaining results
        while 'LastEvaluatedKey' in response:
            response = ddb_table.query(
                KeyConditionExpression=Key('flight_number').eq(flight_number),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            bags.extend(response['Items'])

        result = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": { "Content-Type": "application/json","Access-Control-Allow-Origin":"*" },
                "body": json.dumps(bags)
        }
        return result 
    except ValidationError as e:
        logger.error("Unable to deserialize event: " + str(e.errors()))
        # raise the exception to allow the lambda function to error
        # important for dead-letter queuing
        raise e
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e


'''
Get bags from a specific flight and format the result for API Gateway Proxy Integration
'''
def get_flight_handler(event: object, context):
    try:
        logger.info("Received event: "+ json.dumps(event))
        event_data = model.APIGWEvent(**event)
        flight_number = urllib.parse.unquote(event_data.pathParameters.flight_number)
        logger.info(f"Getting bags from flight {flight_number}")
  
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

        result = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": { "Content-Type": "application/json","Access-Control-Allow-Origin":"*" },
                "body": json.dumps(bags)
        }
        return result 
    except ValidationError as e:
        logger.error("Unable to deserialize event: " + str(e.errors()))
        # raise the exception to allow the lambda function to error
        # important for dead-letter queuing
        raise e
    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e