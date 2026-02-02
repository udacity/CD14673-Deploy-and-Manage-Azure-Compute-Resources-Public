from ..src import app
import boto3
from moto import mock_aws

@mock_aws
def test_handler():
    sns = boto3.client("sns", "us-east-1")
    # Create a topic in the mock environment
    topic = sns.create_topic(Name="test-topic")
    topic_arn = topic['TopicArn']
    app.sns_topic = topic_arn
    app.sns_client = sns

    app.handler({}, None)