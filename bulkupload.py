"""
	README
	Runs on python 2.7.x
	Needs a valid API user account within the organization in which the API calls will be made
	API Credentials must be generated and added as a profile to ~/.veraocde/credentials
	Takes in a CSV file, wherein each row is a  call to be made and each column is a parameter to be passed to the call
	There must be a column called 'apiaction', where the cell is the API call to be made without the '.do' at the end
	See the sample.csv for more details
"""

from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC as VeracodeHMAC
import veracode_api_signing.credentials
from new_api import veracode_api_call as api_call
from csv_in import csvIn
import traceback

# MAIN
################################################################################
api_profile = raw_input("Profile Name: ")
veracode_api_signing.credentials.PROFILE_DEFAULT = api_profile
creds = VeracodeHMAC()

myCSV = csvIn.fromFile()

lineinfo = myCSV.next()
while lineinfo:
	if 'apiaction' in lineinfo:
		try:
			endpoint = lineinfo.pop('apiaction')
			call = api_call(endpoint=endpoint, creds=creds, params=lineinfo)
		except Exception as e:
			print 'Error: %s' % (e)
			print traceback.print_exc()
	lineinfo = myCSV.next()

print '\n=================='
print 'FUNCTION COMPLETED'
print '=================='
