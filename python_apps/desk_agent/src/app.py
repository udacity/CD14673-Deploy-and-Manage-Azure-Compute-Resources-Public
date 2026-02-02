from datetime import datetime, timezone
import json
import logging
from . import model
from . import sample_values
import requests
from faker import Faker
import uuid
import random
import os

# Setup logging with the python module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api_endpoint = os.environ.get('API_ENDPOINT','')
fake = Faker()

# Create a person for the desk agent
# This is global to provide that the same
# agent handles bags for multiple persons
# which will change as the function scales 
# with AWS Lambda
agent = model.Person(
    first_name = fake.unique.first_name(),
    last_name = fake.unique.last_name(),
    id = str(uuid.uuid4()))

# All bags and customers start in DFW. Go Stars!
current_location = sample_values.dallas_terminal_e_bagdrop

'''
This function is invoked periodically from a CloudWatch Events timer to 
simulate new bags being checked in.  All bags will originated from DFW and 
will relate to fake customers that each have between one and three bags.

The completed bag data is posted to a REST API hosted with AWS API Gateway.
This API uses a service integration to publish the request body, which
contains the checked bag data, into an SQS queue for fan-out processing.
'''
def handler(event: object, context):
    try:
        
        # Create a person for the customer/passenger
        customer = model.Person(
            first_name = fake.unique.first_name(),
            last_name = fake.unique.last_name(),
            id = str(uuid.uuid4()))
        
        # customers may have between 1 asnd 3 bags at random
        number_of_checked_bags = random.randint(1, 3)
        
        # generate a fake flight number (between 10 and 100)
        # later it is formatted like AWS0010
        rand_flight_number = random.randint(10,25)

        # build out data for each bag
        for bag_index in range(number_of_checked_bags):
            bag_number = bag_index+1
            bag = model.Checked_Bag(
                checked_in = True,
                retrieved = False,
                customer=customer,
                desk_agent=agent,
                location_history = [],
                current_location = current_location,
                flight_number = f'AWS{rand_flight_number:04d}',
                created = datetime.now(timezone.utc),
                updated = datetime.now(timezone.utc))

            try:
                # Post the bag data to the API so it can be queued in SQS later
                bag_json_str = bag.model_dump_json()
                bag_json = json.loads(bag_json_str)
                
                # to make our DLQ useful, we should corrupt bag records at random
                # give it a one in 3 chance
                shall_corrupt = random.randint(1,3)==3
                if shall_corrupt:
                    bag_json['current_location']=sample_values.corrupt_data

                
                logger.info(f"Posting {bag_json} -> {api_endpoint}")
                response = requests.post(api_endpoint, json=bag_json, headers={'Content-Type':'application/json'})
                if response.status_code == requests.codes.ok:
                    logger.info(f'Posted bag {bag_number} of {number_of_checked_bags} for customer {bag.customer.id}')
                else:
                    raise Exception(f'{response.status_code} -> {response.text}')
            except Exception as e:
                logger.error('Error posting to API: ' +str(e))
                raise e

    except Exception as e:
        logger.error('An unexpected error has occurred: ' + str(e))
        # raise the exception to allow the lambda function to error
        raise e