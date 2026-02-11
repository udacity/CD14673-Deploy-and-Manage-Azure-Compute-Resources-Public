def lambda_handler(event, context):
    # Log the incoming event for debugging
    print("Received event:", event)

    return {
        'statusCode': 200,
        'body': 'Stream processing complete'
    }