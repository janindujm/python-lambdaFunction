import json
import boto3
import logging
import multipart
import base64



logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    response_headers = {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*"
    }

    return {
        'statusCode': 200,
        'headers': response_headers,
        'body': json.dumps({"message": "ok"})
    }