# Import the handler from handler.py
import handler
import boto3
import pytest
from moto import mock_aws


def test_handler():

    event = {"rawImagePath": "s3://fakebucket/upload.png"}

    context = {}

    #TODO: Mock the S3 Client
    

    response = handler.handler(event, context)

    assert response['statusCode'] == 200
    assert response['body'] == 'Image resized successfully'
