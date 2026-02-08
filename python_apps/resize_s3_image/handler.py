import uuid
import boto3

s3_client = boto3.client('s3')

''' Resize the image to the specified width and height '''


def resize_image(image, width: int, height: int):
    # for simplicity, we dont need to return a real resized image
    pass


''' Download the image from S3 '''


def download_image_from_s3(s3_path: str, temp_file_path: str):
    bucket_start = s3_path.find("s3://") + len("s3://")
    bucket_end = s3_path.find("/", bucket_start)
    BUCKET_NAME = s3_path[bucket_start:bucket_end]
    OBJECT_NAME = s3_path[bucket_end + 1:]
    FILE_NAME = temp_file_path
    print(f"Downloading from S3: {BUCKET_NAME}:{OBJECT_NAME} -> {FILE_NAME}")
    s3_client.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)


''' Upload the image to S3 '''


def upload_image_to_s3(s3_path: str, temp_file_path: str) -> None:
    bucket_start = s3_path.find("s3://") + len("s3://")
    bucket_end = s3_path.find("/", bucket_start)
    BUCKET_NAME = s3_path[bucket_start:bucket_end]
    OBJECT_NAME = s3_path[bucket_end + 1:]
    FILE_NAME = temp_file_path
    print(f"Uploading to S3: {FILE_NAME} <- {BUCKET_NAME}:{OBJECT_NAME}")
    s3_client.upload_file(FILE_NAME, BUCKET_NAME, OBJECT_NAME)


''' AWS Lambda handler function '''


def handler(event, context):

    print("Received event:", event)
    if 'rawImagePath' not in event:
        raise ValueError("Event must contain 'rawImagePath'")

    # make a temp file path
    temp_file_path = f"/tmp/{str(uuid.uuid4())}.png"

    # Download the image from S3
    image = download_image_from_s3(event['rawImagePath'], temp_file_path)


    # Resize
    resize_image(image=image, width=800, height=600)

    # Upload the resized image back to S3
    upload_image_to_s3(event['rawImagePath'], temp_file_path)

    return {
        'statusCode': 200,
        'body': 'Image resized successfully'
    }
