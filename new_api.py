import requests, sys, os, json, logging
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC as VeracodeHMAC

class veracode_api_call():
	def __init__(self, endpoint, creds = None, logger = logger(), params = []):
		self.logger = logger
		
		try: self.rownum = 'Line #%s' % (params.pop('rownum'))
		except: self.rownum = 'TEST'

		self.url, self.response_type = self.get_url_from_endpoint(endpoint)

		if creds == None:
			self.auth=VeracodeHMAC(profile = None)
		else: self.auth=(creds)

		self.r = requests.get(url=self.url, auth=self.auth, params=params)
		
		if self.response_type == 'json':
			self.response = json.loads( str( self.r.text ) )
		else:
			self.response = ET.fromstring( self.r.text )

		self.log_activity()

	def get_url_from_endpoint(self, endpoint):
		version_numbers = dict(beginprescan='5.0', beginscan='5.0', createapp='4.0', \
			createbuild='4.0', deleteapp='5.0', deletebuild='5.0', getappinfo='5.0', \
			getapplist='5.0', getbuildinfo='5.0', getbuildlist='5.0', getfilelist='5.0', \
			getpolicylist='5.0', getprescanresults='5.0', getvendorlist='5.0', \
			removefile='5.0', updateapp='5.0', updatebuild='5.0', uploadfile='5.0', \
			detailedreport='4.0', detailedreportpdf='4.0', getappbuilds='4.0', \
			getcallstacks='4.0', summaryreport='4.0', summaryreportpdf='4.0', \
			thirdpartyreportpdf='4.0', getmitigationinfo='', updatemitigationinfo='', \
			createsandbox='5.0', getsandboxlist='5.0', promotesandbox='5.0', updatesandbox='5.0', \
			createuser='3.0', deleteuser='3.0', getuserinfo='3.0', getuserlist='3.0', \
			updateuser='3.0', createteam='3.0', deleteteam='3.0', getteaminfo='3.0', \
			getteamlist='3.0', updateteam='3.0', getcurriculumlist='3.0', gettracklist='3.0', \
			getmaintenancescheduleinfo='3.0', generateflawreport='3.0', downloadflawreport='3.0')

		if endpoint in version_numbers:
			return '%s/%s/%s.do' % ('https://analysiscenter.veracode.com/api', version_numbers[endpoint], endpoint), 'xml'

		else:
			return '%s/%s' % ('https://api.veracode.io/elearning/v1/', endpoint), 'json'

	def get_response(self): return self.response

	def log_activity(self):
		if self.response.tag == 'error':
			self.logger.error( "[{0}]{1}".format(self.rownum, self.response.text) )
		else:
			self.logger.info( "[{0}]{1}".format(self.rownum, 'Success')	)

class logger():
	def __init__(self, filename = 'logs'):
		import logging, os
		logging.root.handlers = []
		logging.getLogger("requests").setLevel(logging.WARNING)
		logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.INFO)

		fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'logs'))
		fileHandler.setFormatter(logFormatter)
		self.logger.addHandler(fileHandler)

		consoleHandler = logging.StreamHandler(sys.stdout)
		consoleHandler.setFormatter(logFormatter)
		self.logger.addHandler(consoleHandler)
		return self.logger