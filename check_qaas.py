import boto3
import json
from collections import OrderedDict
import urllib2
import sys
import StringIO


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
boto3.setup_default_session(profile_name='devel')
client = boto3.client('support')

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
	print json.dumps(results_ordered, indent=4)























check_aws()
