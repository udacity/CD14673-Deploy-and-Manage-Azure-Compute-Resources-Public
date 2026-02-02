from datetime import datetime, timedelta, timezone
from ..src import app
import boto3
from moto import mock_aws

@mock_aws
def test_get_bags_handler():
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
        "code": "bos",
        "description": "test",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    
  
    result = app.get_bags_handler({}, None)
    assert result is not None
    

@mock_aws
def test_get_bag_handler():
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
        "code": "bos",
        "description": "test",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    
  
    result = app.get_bag_handler({
        'pathParameters': {
            'flight_number': "AWS0020",
            'bag_id': "BAG#19b8f511-7f44-4688-966d-7e7e6f18928f#1#1#7651d2f2-c3ed-4a9c-b6f2-85c624d4d872"
        }}, None)
    
    assert result is not None
    
    

@mock_aws
def test_get_flight_handler():
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
        "code": "bos",
        "description": "test",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    
  
    result = app.get_bag_handler({
        'pathParameters': {
            'flight_number': "AWS0020"
        }}, None)
    
    assert result is not None

@mock_aws
def test_dashboard():
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
        "code": "bos",
        "description": "test",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    

    ddb_table.put_item(Item={
        "id": "BAG#ddfdafd-7f44-4688-966d-7e7e6f18928f#1#1#7651d2f2-c3ed-4a9c-b6f2-85c624d4d872",
        "checked_in": True,
        "current_location": {
        "code": "bos",
        "description": "test",
        "lat": "32.88905",
        "lon": "-97.03634",
        "timestamp": "2026-01-18T15:49:23.949575"
        },
        "customer": {
        "id": "19b8f511-7f44-4688-966d-7e7e6f18928f",
        "first_name": "Max",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    
  
    result = app.dashboard_handler({}, None)
    
    assert result is not None
    
@mock_aws
def test_get_wait_time_handler():
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
        "id": "BAG#ddfdafd-7f44-4688-966d-7e7e6f18928f#1#1#7651d2f2-c3ed-4a9c-b6f2-85c624d4d872",
        "checked_in": True,
        "current_location": {
        "code": "bos",
        "description": "test",
        "lat": "32.88905",
        "lon": "-97.03634",
        "timestamp": "2026-01-18T15:49:23.949575"
        },
        "customer": {
        "id": "19b8f511-7f44-4688-966d-7e7e6f18928f",
        "first_name": "Max",
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
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat()
        })
    
  
    result = app.get_wait_time_handler({}, None)
    
    assert result is not None
    