from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC as VeracodeHMAC
from new_api import veracode_api_call as api_call
from csv_in import csvIn
import traceback, logger, ConfigParser, os

# MAIN
################################################################################
api_profile = raw_input("Profile Name: ")

config = ConfigParser.ConfigParser()
config.read( os.path.join('.', 'credentials') )
api_key_id = config.get(api_profile, 'VERACODE_API_KEY_ID')
api_key_secret = config.get(api_profile, 'VERACODE_API_KEY_SECRET')
creds = VeracodeHMAC(api_key_id, api_key_secret)

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
			logger.error(e)
			logger.error( traceback.print_exc() )
	lineinfo = myCSV.next()

print '\n=================='
print 'FUNCTION COMPLETED'
print '=================='
