from ..src import model
from ..src import app
import json
import boto3
from moto import mock_aws
from datetime import datetime

def test_validate_model():
    event_str='''
        {
            "flight":"foo",
            "timestamp":"2026-01-18T15:37:47+0000"
        }
    '''
    event_json = json.loads(event_str)
    event_model_instance = model.FlightMessage(**event_json)
    assert event_model_instance is not None

@mock_aws
def test_handler():
    # Mock DDB
    table_name = 'project_checked_bags'
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "RANGE"},{"AttributeName": "flight_number", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"},{"AttributeName": "flight_number", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    
    ddb_table = dynamodb.Table(table_name)
    
    app.dynamodb=dynamodb
    app.ddb_table = ddb_table

    ddb_table.put_item(Item={
        "id": "BAG#19b8f511-7f44-4688-966d-7e7e6f18928f#1#1#7651d2f2-c3ed-4a9c-b6f2-85c624d4d872",
        "checked_in": True,
        "current_location": {
        "code": "dfw",
        "description": "DFW Terminal E Bag Drop",
        "lat": "32.88905",
        "lon": "-97.03634",
        "timestamp": "2026-01-18T15:49:23.949575"
        },
        "customer": {
        "id": "19b8f511-7f44-4688-966d-7e7e6f18928f",
        "first_name": "Nicole",
        "last_name": "Rowe"
        },
        "desk_agent": {
        "id": "68e3bccd-5156-429a-ace1-4be8d8949cc4",
        "first_name": "Sarah",
        "last_name": "Walker"
        },
        "flight_number": "AWS0020",
        "location_history": [
        ],
        "retrieved": False,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
        })
    
    event_data = model.SNSEvent(
        Records=[
            model.SNSEventRecord(
                Sns=model.SNSObject(
                    Message=json.dumps({
                        'flight':'AWS0020',
                        'timestamp':datetime.now().isoformat()
                    })
                )
            )
        ]
    )
    event_json = event_data.model_dump_json()
    event_dict = json.loads(event_json)
    app.handler(event_dict, None)