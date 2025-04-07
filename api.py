import json
import boto3
import logging
import multipart
import base64
import jwt





logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    headers = {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*"
    }

    body = event["body"]
    isBase64Encoded = bool(event["isBase64Encoded"])

    if isBase64Encoded:
        body = base64.b64encode(body)
    else:
        body = body.encode('utf-8')

    parse = multipart.FormDataParser(body)
    parts = parse.parse()

    hotel_name = parts.get('hotel_name')
    hotel_rating = parts.get('hotel_rating')
    hotel_city = parts.get('hotel_city')
    hotel_price = parts.get('hotel_price')
    file_name = parts.get('filename')
    user_id = parts.get('user_id')
    id_token = parts.get('id_token')

    
    file = parts.get('fileData').file.read()


    token = jwt.decode(id_token, verify = False)
    group = token.get('cognito:groups')

    if group is None or group != 'Admin':
        logger.error('User not in group')
        return {
            'statusCode': 403,
            'headers': headers,
            'body': json.dumps({"message": "User not in group"})
        }

    bucket_name = os.environ.get('bucketname')
    region = os.environ.get('AWS_REGION')

    s3_client = boto3.client("s3", region_name=region)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file
        )
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"message": "Error uploading file"})
        }

    logger.debug('Info')

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({"message": "ok"})
    }