import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('short_url')

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def lambda_handler(event, context):
    print(event)
    # body = json.loads(event['body'])
    # long_url = body.get('url')

    # if not long_url:
    #     return {'statusCode': 400, 'body': 'URL is required'}

    # short_code = generate_code() 
    # print(short_code)

    # table.put_item(Item={"shorturl": short_code, "longUrl": long_url})

    # # Replace with your domain or API base URL if needed
    # short_url = f"https://sdly.com/{short_code}"

    # return {
    #     'statusCode ': 200,
    #     'body': json.dumps({'short_url': short_url}),
    #     'headers': {'Content-Type': 'application/json',
    #     'Access-Control-Allow-Origin': '*'}
    # }
    try:
        print("Event:", event)
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid request body'}),
                'headers': {'Access-Control-Allow-Origin': '*'}
            }

        long_url = body.get('url')
        if not long_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'}),
                'headers': {'Access-Control-Allow-Origin': '*'}
            }

        short_code = generate_code()
        table.put_item(Item={'shorturl': short_code, 'longUrl': long_url})

        short_url = f"https://sdly.com/{short_code}"

        return {
            'statusCode': 200,
            'body': json.dumps({'short_url': short_url}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }






