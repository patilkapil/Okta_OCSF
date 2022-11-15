# Okta_OCSF

### Architecture  

Here’s how to convert incoming Okta System Log JSON data using the AWS Lambda function. Use the format conversion feature of Kinesis Firehose to convert the JSON data into Parquet. 

 ![image](https://user-images.githubusercontent.com/2838125/202000596-978d784c-23d2-474a-b83a-8d14d8527fbf.png)


<b>Step 1</b>: Create integration between Okta and Amazon EventBridge

<b>Step 2 </b>: Define an event rule filter to capture events from Okta System Log and communicate it to Amazon Kinesis Firehose


<b>Step 3 </b>: Firehose stream invokes a Lambda as it receives an event from EventBridge. The Lambda function will transform Okta’s System Log data into OCSF-formatted JSON.


<b>Step 4 </b> : Configure a Firehose data stream to transform Okta System Log into OCSF format by invoking a Lambda function.


<b>Step 5 </b> : Configure a Firehose data stream to convert the OCSF format from step 4 into a parquet record. (Parquet is the only acceptable format for Amazon Security Lake)


<b>Step 6 </b> : Converted Parquet files with OCSF schema will be stored in an S3 bucket as part of Amazon Security Lake. 
		 	 	 		

  
###  Why is this integration guide helpful?

This integration guide provides an automated approach to access Syslogs outside Okta and convert them into an OCSF format for any downstream analytical applications. Using the architecture explained in this post, customers can convert User Assignment/Un-Assignment,  Application Assignment/Un-Assignments, and MFA enrollment log events can be captured and normalized to OCSF schema format.  

### How to use this integration guide?

This integration guide is for customers, data engineers, and developers who want to convert Okta’s Syslogs into OCSF schema format. The architecture pattern in this integration guide will help customers build a data pipeline for Okta Syslogs for a business use case.
 

The integration guide here presents an end-end solution for converting Okta Syslogs events into OCSF schema.
The CloudFormation script provided as part of the documentation helps customers focus on the core transformation logic and not worry about integrating different AWS services. 
Use AWS Lambda code as an example/baseline for performing an OCSF   transformation. AWS Lambda shows how to read and parse Okta’s Syslog event and map it to various categories of OCSF schema. 
The DataCatalog resource in the CloudFormation script maintains a table schema. Please make sure the data catalog schema and JSON output from AWS Lambda match - any discrepancy between these two artifacts could result in an error. 


### Extending/re-using the solution for other security events?

As highlighted, the event considered for this post is successful user authentication in the Okta portal. If you want to extend this to other events, for example, user assignment, user un-assignment, etc. Please follow these steps: 
Get a sample of the Syslogs event Link 
Look at the OCSF Schema Link, and identify where the Okta event belongs. 
Perform the data mapping exercise and map fields between Okta SysLog events to OCSF Schema. (Please refer to the current AWS Lambda for the current mapping)
Modify the AWS Lambda function for the mapping defined in #3
In the CloudFormation, you will need to determine the rule which captures Okta’s Syslog event. Update/Add the event rule in “AWS::Events::Rule” resource.
For consistent and error-free transformation, update the glue data catalog schema from the CloudFormation to be compatible with AWS Lambda output.

## How to map between the Okta System Log events and OCSF schema attributes ?

As discussed in the above use case, the security event we are considering is “Successful Authentication.” As per the current OCSF schema, the event falls under the Audit Activity category. 

Once a targeted event category is identified, refer to the OCSF schema information here OCSF schema. You will notice Authentication [3002] as a category; click it. It will point to the targeted schema, values, descriptions, etc. 

You can start mapping the Okta Syslog event attribute to the destination schema. Here is a sample of mapping between Okta’s Syslog event and OCSF schema. 

<b> <i> Please use the following mapping table as a reference only for schema mapping activity. Always check the latest OCSF schema when converting Okta System logs to OCSF schema. </i></b> 


| Destination - OCSF Format        | Source - Okta system Log           | 
| ------------- |:-------------:|  
| activity_name     |  Check if "user.authentication" (Event Type) is present in data->detail->eventType | 
| activity_id     |  Based on activity value (from row 1) select the activity_id value |   
| auth_protocol | detail - > authenticationContext-> authenticationProvider| 
| auth_protocol_id | Get value from the OCSF schema column description |
| category_name | Audit Activity events. ( For Login Activity) |
| category_uid | Get value from the OCSF schema column description page |
| class_name | Type of event category |
| class_uid | Based on class_name value (from row 9) select the class_uid value |
| is_cleartext | If Authentication protocol from row #5 is not FTP /TELNET value will be FALSE |
| dst_endpoint |  hostname: detail ->debugContext->debugData->requestUri : ip -> "" , instance_uid -> "" ,interface_id -> "",svc_name -> detail ->debugContext->debugData->url |
| dst_user | detail->actor ->alternateID |
| enrichments | detail ->target |
| time | detail ->time |
| logon_type | detail->transaction->type |
| logon_type_id | detail->transaction->type ==Web then -1 |
| message | detail-> displayMessage |
| ref_time | time |
| profiles | detail->actor->alternateId |
| session_uid | detail-> authenticationContext-> externalSessionID |
| severity | detail->info |
| severity_id | detail->info Prase for int values based on OCSF schema|
| src_endpoint | hostname: detail ->debugContext->debugData->requestUri,ip -> detail->client->userAgebt->IP, interface_id - > detail->client->userAgebt->device |
| user | detail->actor->type,detail->actor-> displayname , detail-> actor- > alternateID |
| status | detail-> Outcome |
| status_detail | detail-> Outcome |
| status_id | detail-> Outcome Parse and int |
| type_name | Check if "user.authentication" (Event Type) is present in data['detail']['eventType'] |
| unmapped  | JSON array ; values that are not mapped and are important for analysis purposes |
| user user | detail-> target[0]->alternateID |
| metadata  | data['time'] ,data['version'] |



