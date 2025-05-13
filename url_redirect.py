import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('short_url')

def lambda_handler(event, context):
    print(event)
    short_code = event['pathParameters']['short_code']
    print(short_code)

    y = short_code.replace("%7B","")

    z = y.replace("%7D","")

    print(z)
    
    try:
        response = table.get_item(Key={'shorturl': z})
        print("response:" , response)
        item = response.get('Item')

        print(item)

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Short URL not found'}),
                'headers': {'Content-Type': 'application/json'}
            }

        return {
            'statusCode': 301,
            'headers': {
                'Location': item['longUrl']
            },
            'body': ''
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Server error', 'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
