from __future__ import print_function # Python 2/3 compatibility

import boto3
import json
import decimal
import requests
import time
import config



def getStores(zipcode):
    # Set the URL
    url = "http://api.walmartlabs.com/v1/stores?format=json&zip=" + str(zipcode).zfill(5) + "&apiKey=" + config.api_key

    # Request the information from Walmart Open API
    resp = requests.get(url)
    parsed_json = resp.json()

    # Slow down the requests
    time.sleep(1)

    # Return the result
    return parsed_json



# Main 

def getStoreZips():
    D = {}
    rateLimit = 5000

    # Load the json file with all the zip codes from the US
    with open("uspostalcodes.json") as json_file:
        locations = json.load(json_file, parse_float = decimal.Decimal)
        
        # for each postal code, query the Walmart API to get the nearby store and zip code
        for location in locations:
            zipcode = int(location['zipcode'])

            print("Adding zipcode:", str(zipcode).zfill(5))

            # get all the stores
            storesByZip = getStores(zipcode)

            rateLimit = rateLimit - 1

            print('rate---->', rateLimit)

            # create the dictionary
            for store in storesByZip:
                try:
                    D[store['no']] = store['zip']
                except:
                    # Return if JSON didn't provide an answer
                    print ('JSON didnt retrieve the data')
                    return D

            # Return if rateLimit
            if rateLimit == 0:
                return D

        # Normal path
        return D


# MAIN APPLICATION
D = getStoreZips()

# Connect to AWS DynamoDB and complete the information
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('walmart')

# Insert the items from the dictionary into table
for no,zipcode in D.items():
    print(no,':',zipcode)
    jsonString = { "no": no,  "zipcode": zipcode}

    try:
        response = table.put_item( Item=jsonString )
    except:
        print('Dynamo Put Item error', jsonString)