import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "WishList"
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    http_method = event['requestContext']['httpMethod']
    
    if http_method == "GET":
        try:
            # Scan the table
            response = table.scan()
            items = response.get('Items', [])
            
            return {
                'statusCode': 200,
                'body': json.dumps(items),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    
    elif http_method == "POST":
        try:
            # Parse the request body
            body = json.loads(event['body'])
            name = body.get('name')
            url = body.get('url')
            description = body.get('description')
            
            # Put item in the table
            item = {
                'id': context.aws_request_id,
                'name': name,
                'url': url,
                'description': description
            }
            table.put_item(Item=item)
            
            return {
                'statusCode': 201,
                'body': json.dumps({'id': context.aws_request_id}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unsupported HTTP method'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
