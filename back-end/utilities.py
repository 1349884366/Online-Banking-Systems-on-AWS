import datetime
import boto3
from boto3.dynamodb.conditions import Key
import base64
import uuid

session = boto3.session.Session()
kms = session.client('kms')
user_table = boto3.resource('dynamodb').Table('User')
dynamodb_c = boto3.client('dynamodb')
key = 'alias/eBankCMK'


def encryption(data):
    data_e = kms.encrypt(
    # The identifier of the CMK to use for encryption. You can use the key ID or Amazon Resource Name (ARN) of the CMK, or the name or ARN of an alias that refers to the CMK.
    KeyId=key,
    # The data to encrypt.
    Plaintext=data,)
    binary_data = data_e[u'CiphertextBlob']
    encrypted_data = base64.b64encode(binary_data)
    return encrypted_data.decode()
#define the decryption
def decryption(data):
    binary_data = base64.b64decode(data.encode())
    meta = kms.decrypt(CiphertextBlob=binary_data)
    plaintext = meta[u'Plaintext']
    return plaintext.decode()
    
def check_auth(Auth_key,email):
    de_auth = decryption(Auth_key)
    tmp = de_auth.split("+", 1)
    date_auth = datetime.datetime.strptime(tmp[1], '%Y-%m-%d %H:%M:%S.%f')
    date_now = datetime.datetime.now()
    time_delta = (date_now - date_auth)
    total_seconds = time_delta.total_seconds()
    hours = total_seconds/3600
    if (email == tmp[0] and hours <= 8):
        return True
    else:
        return False
        
#define Transaction database operation        
def db_trans(data):
#set up the data
    sender = data['Sender']
    reciever = data['Reciever']
    money = data['Money']
    operation_str = " Transfer "+str(money)+"$ to "+str(reciever)
    operation_str_reciever = "Get " + str(money)+"$ from "+str(sender)
#get the database version
    response_s = user_table.query(ConsistentRead=True,KeyConditionExpression=Key('User_ID').eq(sender))
    response_r = user_table.query(ConsistentRead=True,KeyConditionExpression=Key('User_ID').eq(reciever))
    s_v = response_s['Items'][0]['Ver']
    new_sv= str(int(s_v) + 1)
    s_b = str(int(response_s['Items'][0]['Balance'])-int(money))
    r_v = response_r['Items'][0]['Ver']
    new_rv= str(int(r_v) + 1)
    r_b = str(int(response_r['Items'][0]['Balance'])+int(money))
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())
    uuid3 = str(uuid.uuid4())
    try:
        resp = dynamodb_c.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "Transactions",
                        "Item": {
                            "Transaction_ID": {"S": uuid1},
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
                            "Activity_ID": {"S": uuid2},
                            "User": {"S": sender},
                            "Opeartion": {"S": operation_str},
                            "Time": {"S": datetime.datetime.now().isoformat()}
                        },
                    },
                },
                {
                    "Put": {
                        "TableName": "Activities",
                        "Item": {
                            "Activity_ID": {"S": uuid3},
                            "User": {"S": reciever},
                            "Opeartion": {"S": operation_str_reciever},
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
        
#define Deposit database operation
def db_dep(data):
#set up the data
    user = data['UserID']
    money = data['Money']
    operation_str = "Deposit "+str(money)+"$"
#get the database version
    response = user_table.query(ConsistentRead=True,KeyConditionExpression=Key('User_ID').eq(user))
    ver = response['Items'][0]['Ver']
    new_ver= str(int(ver) + 1)
    new_b = str(int(response['Items'][0]['Balance'])+int(money))
    uuid1 = str(uuid.uuid4())
    try:
        resp = dynamodb_c.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "Activities",
                        "Item": {
                            "Activity_ID": {"S": uuid1},
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