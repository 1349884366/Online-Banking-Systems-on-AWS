# import the JSON utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
# import package to help us with dates and date formatting
import datetime
import base64

import APIfunctions
 

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
dynamodb_c = boto3.client('dynamodb')
# use the DynamoDB object to select our table
user_table = dynamodb.Table('User')
act_table = dynamodb.Table('Activities')
trans_table = dynamodb.Table('Transactions')


   

# define the handler function that the Lambda service will use an entry point
def lambda_handler(event, context):
# extract values from the event object we got from the Lambda service
    operation = event['Opeartion']
    if (operation == 'Login'):
        return APIfunctions.login(event)
    elif (operation == 'Signup'):
        return APIfunctions.signup(event)
    elif (operation == 'Trans'):
        return APIfunctions.trans(event)
    elif (operation == 'Deposit'):
        return APIfunctions.deposit(event)
    elif (operation == 'Activities'):
        return APIfunctions.act(event)
    elif (operation == 'TransHis'):
        return APIfunctions.TransHis(event)
    


    

        
# def TransHis(data):
# #get input
#     email = data['Email']
#     Auth_key = data['Auth_key']
# #check auth key
#     de_auth = decryption(Auth_key)
#     tmp = de_auth.split("+", 1)
#     auth_data = tmp[1]
#     date_2 = datetime.datetime.strptime(auth_data, '%Y-%m-%d %H:%M:%S.%f')
#     time_delta = (date_now - date_2)
#     total_seconds = time_delta.total_seconds()
#     hours = total_seconds/3600
# #get the Transactions
#     if (email == tmp[0] and hours <= 8 ):
#         response_trans = trans_table.query(
#             KeyConditionExpression=Key('Transaction_ID').eq(email))
#         trans_lst = []
#         for i in response_trans['Items']:
#             trans_lst.append(("Date: "+str(i['Time']).split(".")[0] +"   Opeartion: "+ str(i['Sender'])+" transfer "+str(i['Money'])+"$ to "+str(i['Reciever']) ))
#         return {
#             'statusCode': 200,
#             'body': json.dumps({"Transcations":json.dumps(trans_lst)})
#             }
#     else:
#         return{
#         'statusCode': 401,
#         'body': json.dumps({"Description": "Unauthorized"})
#         }
    
    
        
# return a properly formatted JSON object