# 7park Walmart

# loaddata.py
Does a reverse engineer to get the stores related to zipcodes.
- For each zipcode based on the US postal service list
  - Get all the nearby stores and create a dictionary (key=store, value=zip).
  - Insert the dictionary in dynamoDB table walmart.

Requeriments: 
- Python 3.7
- Libraries requested in the import installed (pip install)
- AWS CLI installed and configured with credentials to access DynamoDB.
- Create a table called 'walmart' in DynamoDB with 'no' numeric as hash key.
- You need a Walmart api key save in a file config.py (not uploaded for security)


# readdata.py
Function that returns the zipcode of a given store id.

Requirements:
- This is the source of what is running in AWS Lambda.
- AWS Lambda function need to have access to DynamoDB table walmart.
- AWS API Gateway configured to invoke the lambda function.

Ex: 
https://ewn7lusnh8.execute-api.us-east-1.amazonaws.com/PROD/?no=994
