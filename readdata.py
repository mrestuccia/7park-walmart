import boto3
from boto3.dynamodb.conditions import Key, Attr

# this has been deployed to AWS Lambda
# API Gateway: https://ewn7lusnh8.execute-api.us-east-1.amazonaws.com/PROD/?no={storeid}
# Find a zip code given a store no
def findZip(no):
    # Connect to dynamo
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('walmart')
 
    # Create the json object
    jsonString = {"no": no}
 
    try:
        # Read the information
        response = table.get_item(Key=jsonString)
    except:
        # Log Error
        print('Error in getting the information for store ' + no)
    else:
        if 'Item' in response:
            return response['Item']
            
    return None 


# Main Function
def lambda_handler(event, context):
    # Check if store no came as parameter
    if 'no' in event:
        # Find the zip code
        return findZip(event['no'])
    else:
        return None