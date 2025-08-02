import json

def handler(event, context):
    """Simple test function"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps({
            'message': 'Test function works!',
            'method': event.get('httpMethod', 'GET'),
            'path': event.get('path', 'unknown')
        })
    }