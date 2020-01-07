from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC as VeracodeHMAC
import veracode_api_signing.credentials
from new_api import veracode_api_call as api_call
import logger
from csv_in import csvIn
import traceback

# MAIN
################################################################################
api_profile = raw_input("Profile Name: ")
veracode_api_signing.credentials.PROFILE_DEFAULT = api_profile
creds = VeracodeHMAC()

filename = raw_input("CSV File: ")
myCSV = csvIn.fromFile(filename)
logger = logger.Logger(filename)

lineinfo = myCSV.next()
while lineinfo:
	if 'apiaction' in lineinfo:
		try:
			endpoint = lineinfo.pop('apiaction')
			call = api_call(endpoint=endpoint, creds=creds, logger=logger, params=lineinfo)
		except Exception as e:
			print 'Error: %s' % (e)
			print traceback.print_exc()
	lineinfo = myCSV.next()

print '\n=================='
print 'FUNCTION COMPLETED'
print '=================='
