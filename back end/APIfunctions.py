import boto3
from boto3.dynamodb.conditions import Key
import datetime
import utilities
import json
import uuid

user_table = boto3.resource('dynamodb').Table('User')
act_table = boto3.resource('dynamodb').Table('Activities')
trans_table = boto3.resource('dynamodb').Table('Transactions')
uuid = str(uuid.uuid4())

#define login function
def login(data):
    #define the email and password from client input
    email = data['Email']
    password = data['Password']
    #query the user table to get
    response = user_table.query(
    KeyConditionExpression=Key('User_ID').eq(email)
    )
    user = response['Items'][0]
    date_now = datetime.datetime.now()
    auth_str = str(user['Email']) + "+" +str(date_now)
    en_auth = utilities.encryption(auth_str)
    de_auth = utilities.decryption(en_auth)
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
    KeyConditionExpression=Key('User_ID').eq(email)
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
            'Balance':"100",
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
        'body': json.dumps({"Description": "Unknown Error"})
        }


#define Trans function        
def trans(data):
#decryption the input data
    sender = data['Sender']
    reciever = data['Reciever']
    money = data['Money']
    Auth_key = data['Auth_key']
#check auth key
    validation = utilities.check_auth(Auth_key,sender)
#check the validation of the operation
    if (validation and int(money)>0):
        response = user_table.query(KeyConditionExpression=Key('User_ID').eq(sender))
        balance = response['Items'][0]['Balance']
        if( int(int(balance) - int(money)) >=0 ):
            res = utilities.db_trans(data)
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
    
#define Deposit function
def deposit(data):
#decryption the input data
    user = data['UserID']
    money = data['Money']
    Auth_key = data['Auth_key']
    Attachment = data["Attachment"]
#check auth key
    validation = utilities.check_auth(Auth_key,user)
#check the validation of the operation
    if (validation and int(money)>0):
        res = utilities.db_dep(data)
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
        'body': json.dumps({"Description": "Unauthorized"})
        }
        
def act(data):
#get input
    email = data['Email']
    Auth_key = data['Auth_key']
#check auth key
    validation = utilities.check_auth(Auth_key,email)
#get the Activities
    if (validation):
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
    validation = utilities.check_auth(Auth_key,email)
#get the Transactions
    if (validation):
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