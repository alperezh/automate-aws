import json
import boto3
from collections import OrderedDict
import urllib2
import sys
import os
import StringIO
import datetime



def lambda_handler(event, context):
    # TODO implement
    results_ordered = []
    tests = { 
    "ELB Security Groups" : "xSqX82fQu",
    "ELB Listener Security" : "a2sEc6ILx",
    "Exposed Access Keys" : "12Fnkpl8Y5",
    "IAM Password Policy" : "Yw2K9puPzl",
    "IAM Use" : "zXCkfM1nI3",
    "Security Groups - Specific Ports Unrestricted" : "HCP4007jGY",
    "Security Groups - Unrestricted Access" : "1iG5NDGVre",
    "AWS CloudTrail Logging" : "vjafUGJ9H0"
        
    }
    
    results = [] 
    boto3.setup_default_session
    client = boto3.client('support')
    bucket_name = "qaas-result-collector-753358023111-eu-west-1"
    s3 = boto3.resource('s3')
    
    def check_aws():
	    
	    for i in tests:
		    y = {}
		    response = client.describe_trusted_advisor_check_result(
   		    checkId=tests[i],
   		    language='en'
		    )
	
		    y['name'] = i 
		    y['status'] = response['result']['status']
		    y['total'] = response['result']['resourcesSummary']['resourcesProcessed']
		    y['errors'] = response['result']['resourcesSummary']['resourcesFlagged']
		    y['timestamp'] = response['result']['timestamp']
		    results.append(dict(y))

	    sort_order = ['name', 'status', 'errors', 'total', 'timestamp']
	    results_ordered = [OrderedDict(sorted(item.iteritems(), key=lambda (k, v): sort_order.index(k)))
                    for item in results]
	    rest = json.dumps(results_ordered, indent=4)
	    f = open("/tmp/sec-report.json","w")
	    f.write(rest)
	    f.close()
        
    
    check_aws()
    if os.path.exists("/tmp/sec-report.json"):
        s3.meta.client.upload_file('/tmp/sec-report.json', bucket_name, 'bigfinite/security/sec-report.json' + "." + str(datetime.datetime.now()))
    
    
