# import the JSON utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
from boto3.dynamodb.conditions import Key
# import package to help us with dates and date formatting
import datetime
import base64
#define the encryption
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()
#define the decryption
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
   
str_text = "123456wae"
#define the encryption key
key = "xzasdffasfsf"
en_text = encode(key,str_text)
de_text = decode(key,en_text)


# store the current time in a human readable format in a variable
date_time_str = '2021-03-31 00:43:13.539780'
date_2 = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
date_now = datetime.datetime.now()
time_delta = (date_now - date_2)
total_seconds = time_delta.total_seconds()
hours = total_seconds/3600
 

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
user_table = dynamodb.Table('User')
act_table = dynamodb.Table('Activities')
trans_table = dynamodb.Table('Transactions')

# define the handler function that the Lambda service will use an entry point
def lambda_handler(event, context):
# extract values from the event object we got from the Lambda service
    operation = event['Opeartion']
    if (operation == 'Login'):
        return login(event)
    elif (operation == 'Signup'):
        return signup(event)
    # elif (operation == 'Trans'):
    #     trans(event)
    # elif (operation == 'Deposit'):
    #     deposit(event)
    # else:
    #     return{
    #     'statusCode': 400,
    #     'body': None
    #     }
    
#define login function
def login(data):
    #define the email and password from client input
    email = data['Email']
    password = data['Password']
    #query the user table to get
    response = user_table.query(
    IndexName='Email-index',
    KeyConditionExpression=Key('Email').eq(email)
    )
    user = response['Items'][0]
    auth_str = str(user['Email']) + "+" +str(date_now)
    en_auth = encode(key,auth_str)
    de_auth = decode(key,en_auth)
    if user['Password'] == password:
        name = user['Name']
        balance = user['Balance']
        return {
        'statusCode': 200,
        'body': json.dumps({"name": name,"balance": balance,"auth": en_auth})
        }
    else:
        return{
        'statusCode': 401,
        'body': None
        }
        
#define signup function
def signup(data):
    name = data['Name']
    email = data['Email']
    password = data['Password']
    
    response = user_table.query(
    IndexName='Email-index',
    KeyConditionExpression=Key('Email').eq(email)
    )
    if len(response['Items']) > 0:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "Email exists"})
        }
    elif len(response['Items']) == 0:
        response = user_table.put_item(
            Item={
            'User_ID': email,
            'Name': name,
            'Email':email,
            'Balance':"0",
            'Password':password})
        return{
        'statusCode': 201,
        'body': json.dumps({"Description": "Success"})
        }
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "error"})
        }
        
# def trans(data):

# def deposit(data):
    
        
# return a properly formatted JSON object