import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    # Log the incoming event for debugging
    print(f"Received event: {json.dumps(event)}")

    for record in event['Records']:
        sns_message = json.loads(record['body'])
        order = json.loads(sns_message['Message'])

        print(f"Received order: {order}")

        try:
            table.put_item(
                Item={
                    'orderId': order['orderId'],
                    'userId': order['userId'],
                    'itemName': order['itemName'],
                    'quantity': order['quantity'],
                    'status': order['status'],
                    'timestamp': order['timestamp']
                }
            )
            print(f"Inserted order {order['orderId']}")
        except Exception as e:
            print(f"Insert failed: {e}")
            raise e
