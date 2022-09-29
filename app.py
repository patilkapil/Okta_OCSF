import base64
import json
from datetime import date

import pandas as pd

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    output=[]
    for record in event['records']:
        recordId = record['recordId']
        data = base64.b64decode(record['data'])
        data = json.loads(data.decode('utf8'))
        #Base 64 encoded strings
        #data = [['tom', 10], ['nick', 15], ['juli', 14]]
        result=tranform_data(data)
        #result = output1.to_json(orient="split")
        #print('typeeeeeeee')
        print(type(output))

        output_record = {
            'recordId': record['recordId'], # is this the problem? I used sequenceNumber, it is not right.
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(result, separators=(',', ':')).encode('utf-8') + b'\n').decode(
                'utf-8')

        }
        output.append(output_record)

    print(output)
    return {'records': output}
    #return {'records': output}

    '''
    bytes_encoded = bytes_encoded.encode(encoding='utf-8')
    print(bytes_encoded)
    #data=recordId.decode()
    str_decoded = bytes_encoded.decode()
    print(str_decoded)

    str_decoded = bytes_encoded.decode()
    print(type(str_decoded))

    return {
    "statusCode": 200,
    "body": json.dumps({
        "message": "hello world"
        # "location": ip.text.replace("\n", "")
    })
    }'''


def get_activity_details(activityInfo):
    activity = "Unknown"
    activity_id = 0
    if "user.authentication" in activityInfo:
        print('inside activity')
        activity='Logon'
        activity_id=1
    return activity,activity_id


def get_auth_protocol(authProviderDetail):
    auth_protocol = "Unknown"
    auth_protocol_id = 0
    if "FACTOR" in authProviderDetail:
        print('inside auth protocol')
        auth_protocol = "Other  / MFA"
        auth_protocol_id = 1
    return auth_protocol,auth_protocol_id


def get_category():
    category_name='Audit Activity events'
    category_uid=3
    return category_name,category_uid


def get_class():
    class_name="Authentication Audit"
    class_uid= 3002
    return class_name,class_uid


def get_clearText_value(auth_protocol):
    is_clearText=False
    if ((auth_protocol!='FTP') and (auth_protocol!='TELNET')):
        is_clearText==True

    return is_clearText


def get_destination_endPoint(destination_endpoint):

    detination_details={"hostname":destination_endpoint['requestUri'],
    "ip":"",
    "instance_uid":"",
    "interface_id":"",
    "svc_name":destination_endpoint['url']}
    return detination_details


def get_logon_type(login_transaction):
    logon_type=login_transaction['type']
    logon_type_id=0
    if "WEB" in logon_type:
        logon_type_id=-1
    return  logon_type,logon_type_id


def get_severity(severity):
    severity_id = -1
    if "INFO" in severity:
        severity_id=1
    return  severity,severity_id


def get_src_endpoint(data):
    src_end_point={
    "hostname": data['debugContext']['debugData']['requestUri'],
    "ip ": data['client']['ipAddress'],
    "interface_id": data['client']['device']
    }
    return src_end_point


def get_src_user(data):
    src_user={
        'type':data['actor']['type'],
        'displayname':data['actor']['displayName'],
        'alternateID':data['actor']['alternateId']
    }
    return src_user


def get_status_details(data):
    status=data['outcome']['result']
    status_code	='N/A'
    status_detail=''
    status_id=-1
    if "SUCCESS" in status:
        status_detail="LOGON_USER_INITIATED"
        status_id=1

    return status,status_code,status_detail,status_id


def tranform_data(data):
    #get activity


    activity,activity_id=get_activity_details(data['detail']['eventType'])
    auth_protocol,auth_protocol_id=get_auth_protocol(data['detail']['authenticationContext']['authenticationProvider'])
    category_name,category_uid=get_category()
    class_name,class_uid=get_class()
    is_cleartext=get_clearText_value(auth_protocol)
    dst_endpoint=get_destination_endPoint(data['detail']['debugContext']['debugData'])
    dst_user=data['detail']['actor']['alternateId']
    enrichments=data['detail']['target']
    _time=data['time']
    logon_type,logon_type_id=get_logon_type(data['detail']['transaction'])
    displayMessage=data['detail']['displayMessage']
    ref_time=data['time']
    profile=data['detail']['actor']['alternateId']
    session_uid=data['detail']['authenticationContext']['externalSessionId']
    severity,severity_id=get_severity(data['detail']['severity'])
    src_endpoint=get_src_endpoint(data['detail'])
    src_user=get_src_user(data['detail'])
    status,status_code,status_detail,status_id = get_status_details(data['detail'])
    type_uid='300201' #HardCoded
    type_name='Authentication Audit: Logon'

    json_data={

        'activity':activity,
        'activity_id':activity_id,
        'auth_protocol':auth_protocol,
        'auth_protocol_id':auth_protocol_id,
        'category_name':category_name,
        'category_uid':category_uid,
        'class_name':class_name,
        'class_uid':class_uid,
        'is_cleartext':is_cleartext,
        'dst_endpoint':dst_endpoint,
        'dst_user':dst_user,
        'enrichments':enrichments,
        '_time':_time,
        'logon_type':logon_type,
        'logon_type_id':logon_type_id,
        'displayMessage':displayMessage,
        'ref_time':ref_time,
        'profile':profile,
        'session_uid':session_uid,
        'severity':severity,
        'severity_id':severity_id,
        'src_endpoint':src_endpoint,
        'src_user':src_user,
        'status':status,
        'status_code':status_code,
        'status_detail':status_detail,
        'status_id':status_id,
        'type_uid':type_uid,
        'type_name':type_name

    }
    '''data=[[activity,activity_id,auth_protocol,auth_protocol_id,category_name,category_uid,class_name,class_uid,is_cleartext,destination_endpoint,dst_user,enrichments,_time,logon_type,
           logon_type_id,displayMessage,ref_time,profile,session_uid,severity,severity_id,src_endpoint,src_user,status,status_code,
           status_detail,status_id,type_uid,type_name]]
    # data = [['tom', 10], ['nick', 15], ['juli', 14]]
    #get
    df = pd.DataFrame(data, columns=['activity','activity_id','auth_protocol','auth_protocol_id','category_name','category_uid','class_name','class_uid','is_cleartext','dst_endpoint',
                                     'dst_user','enrichments','_time','logon_type','logon_type_id','displayMessage','ref_time','profile','session_uid','severity','severity_id',
                                     'src_endpoint','src_user','status','status_code','status_detail','status_id','type_uid','type_name'])
    '''
    #df.to_csv("data.csv")
    #df.to_csv("/tmp/data.csv", index=False,sep='\t', encoding='utf-8')
    '''output=[]
    output_record = {
        'result': 'Ok',
        'data': data

     }
    output.append(output_record)'''

    return json_data
    #return "data"