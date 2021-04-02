# import the JSON utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
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
        return login(event)
    elif (operation == 'Signup'):
        return signup(event)
    elif (operation == 'Trans'):
        return trans(event)
    elif (operation == 'Deposit'):
        return deposit(event)
    elif (operation == 'Activities'):
        return act(event)
    elif (operation == 'TransHis'):
        return TransHis(event)
    # else:
    #     return{
    #     'statusCode': 400,
    #     'body': None
    #     }
    
def act(data):
#get input
    email = data['Email']
    Auth_key = data['Auth_key']
#check auth key
    de_auth = decode(key,Auth_key)
    tmp = de_auth.split("+", 1)
    auth_data = tmp[1]
    date_2 = datetime.datetime.strptime(auth_data, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = (date_now - date_2)
    total_seconds = time_delta.total_seconds()
    hours = total_seconds/3600
#get the Activities
    if (email == tmp[0] and hours <= 8 ):
        response_act = act_table.query(
            KeyConditionExpression=Key('Activity_ID').eq(email))
        act_lst = []
        for i in response_act['Items']:
            act_lst.append(("Date: "+str(i['Time']).split(".")[0]+" Opeartion: "+str(i['Opeartion']) ))
        return {
            'statusCode': 200,
            'body': json.dumps({"Activities":json.dumps(act_lst)})
            }
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "Unauthorized"})
        }
        
def TransHis(data):
#get input
    email = data['Email']
    Auth_key = data['Auth_key']
#check auth key
    de_auth = decode(key,Auth_key)
    tmp = de_auth.split("+", 1)
    auth_data = tmp[1]
    date_2 = datetime.datetime.strptime(auth_data, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = (date_now - date_2)
    total_seconds = time_delta.total_seconds()
    hours = total_seconds/3600
#get the Transactions
    if (email == tmp[0] and hours <= 8 ):
        response_trans = trans_table.query(
            KeyConditionExpression=Key('Transaction_ID').eq(email))
        trans_lst = []
        for i in response_trans['Items']:
            trans_lst.append(("Date: "+str(i['Time']).split(".")[0] +"   Opeartion: "+ str(i['Sender'])+" transfer "+str(i['Money'])+"$ to "+str(i['Reciever']) ))
        return {
            'statusCode': 200,
            'body': json.dumps({"Transcations":json.dumps(trans_lst)})
            }
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "Unauthorized"})
        }
    
    
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
            'Password':password,
            'Ver': "0",
            })
        return{
        'statusCode': 201,
        'body': json.dumps({"Description": "Success"})
        }
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "error"})
        }

#define Trans function        
def trans(data):
#decode the input data
    sender = data['Sender']
    reciever = data['Reciever']
    money = data['Money']
    Auth_key = data['Auth_key']
#check auth key
    de_auth = decode(key,Auth_key)
    tmp = de_auth.split("+", 1)
    auth_data = tmp[1]
    date_2 = datetime.datetime.strptime(auth_data, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = (date_now - date_2)
    total_seconds = time_delta.total_seconds()
    hours = total_seconds/3600
    
#check the validation of the operation
    if (sender == tmp[0] and hours <= 8 and int(money)>0):
        response = user_table.query(IndexName='Email-index',KeyConditionExpression=Key('Email').eq(sender))
        balance = response['Items'][0]['Balance']
        if( int(int(balance) - int(money)) >=0 ):
            res = db_trans(data)
            if (res == True):
                return{
                'statusCode': 200,
                'body': json.dumps({"Description": "Transaction success"})
                }
            else:
                return{
                'statusCode': 401,
                'body': json.dumps({"Description": res})
                }
        else:
            return{
            'statusCode': 401,
            'body': json.dumps({"Description": "You don't have enough money"})
            }
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": "Unauthorized"})
        }
    return data
#define trans database operation
def db_trans(data):
#set up the data
    sender = data['Sender']
    reciever = data['Reciever']
    money = data['Money']
    operation_str = str(sender)+" transfer "+str(money)+"$ to "+str(reciever)
#get the database version
    response_s = user_table.query(IndexName='Email-index',KeyConditionExpression=Key('Email').eq(sender))
    response_r = user_table.query(IndexName='Email-index',KeyConditionExpression=Key('Email').eq(reciever))
    s_v = response_s['Items'][0]['Ver']
    new_sv= str(int(s_v) + 1)
    s_b = str(int(response_s['Items'][0]['Balance'])-int(money))
    r_v = response_r['Items'][0]['Ver']
    new_rv= str(int(r_v) + 1)
    r_b = str(int(response_r['Items'][0]['Balance'])+int(money))
    try:
        resp = dynamodb_c.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "Transactions",
                        "Item": {
                            "Transaction_ID": {"S": sender},
                            "Sender": {"S": sender},
                            "Reciever": {"S": reciever},
                            "Money": {"S": money},
                            "Time": {"S": datetime.datetime.now().isoformat()}
                        },
                    },
                },
                {
                    "Put": {
                        "TableName": "Activities",
                        "Item": {
                            "Activity_ID": {"S": sender},
                            "User": {"S": sender},
                            "Opeartion": {"S": operation_str},
                            "Time": {"S": datetime.datetime.now().isoformat()}
                        },
                    },
                },
                {
                    "Update": {
                        "TableName": "User",
                        "Key": {"User_ID": {"S": sender}},
                        "UpdateExpression": "SET Balance = :b1, Ver = :new_ver",
                        "ExpressionAttributeValues": {
                            ":b1": { "S": s_b },
                            ":s_v": { "S": s_v },
                            ":new_ver": { "S": new_sv }
                        },
                        "ConditionExpression": "Ver = :s_v",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                },
                {
                    "Update": {
                        "TableName": "User",
                        "Key": {"User_ID": {"S": reciever}},
                        "UpdateExpression": "SET Balance = :b2 , Ver = :new_ver",
                        "ExpressionAttributeValues": {
                            ":b2": { "S": r_b },
                            ":r_v": { "S": r_v },
                            ":new_ver": { "S": new_rv }
                        },
                        "ConditionExpression": "Ver = :r_v",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                }
            ]
        )
        return True
    except Exception as e:
        return str(e)
    
    
#define Deposit function
def deposit(data):
#decode the input data
    user = data['UserID']
    money = data['Money']
    Auth_key = data['Auth_key']
    Attachment = data["Attachment"]
#check auth key
    de_auth = decode(key,Auth_key)
    tmp = de_auth.split("+", 1)
    auth_data = tmp[1]
    date_2 = datetime.datetime.strptime(auth_data, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = (date_now - date_2)
    total_seconds = time_delta.total_seconds()
    hours = total_seconds/3600
    
#check the validation of the operation
    if (user == tmp[0] and hours <= 8 and int(money)>0):
        res = db_dep(data)
        if (res == True):
            return{
            'statusCode': 200,
            'body': json.dumps({"Description": "Deposit success"})
            }
        else:
            return{
            'statusCode': 401,
            'body': json.dumps({"Description": res})
            }
            
    else:
        return{
        'statusCode': 401,
        'body': json.dumps({"Description": type(money)})
        }
  
#define Deposit database operation
def db_dep(data):
#set up the data
    user = data['UserID']
    money = data['Money']
    operation_str = "deposit "+str(money)+"$"
#get the database version
    response = user_table.query(IndexName='Email-index',KeyConditionExpression=Key('Email').eq(user))
    ver = response['Items'][0]['Ver']
    new_ver= str(int(ver) + 1)
    new_b = str(int(response['Items'][0]['Balance'])+int(money))
    try:
        resp = dynamodb_c.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "Activities",
                        "Item": {
                            "Activity_ID": {"S": user},
                            "User": {"S": user},
                            "Opeartion": {"S": operation_str},
                            "Time": {"S": datetime.datetime.now().isoformat()}
                        },
                    },
                },
                {
                    "Update": {
                        "TableName": "User",
                        "Key": {"User_ID": {"S": user}},
                        "UpdateExpression": "SET Balance = :b2 , Ver = :new_ver",
                        "ExpressionAttributeValues": {
                            ":b2": { "S": new_b },
                            ":ver": { "S": ver },
                            ":new_ver": { "S": new_ver }
                        },
                        "ConditionExpression": "Ver = :ver",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                }
            ]
        )
        return True
    except Exception as e:
        return str(e)
    
        
# return a properly formatted JSON object