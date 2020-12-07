import hashlib
import pprint
import time

from .client import Clients
from .exceptions import PyForEchoException

class Surveys(object):
	def __init__(self, requests_class, logger):
		""" Init Survey object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger
		self.md5_pw = "a812801c81bdf2"

	def make_digest(self, phone, survey_id):
		dig_ = ''.join([self.md5_pw, phone, str(survey_id)])
		dig = dig_.encode()
		m = hashlib.md5(dig)
		return m.hexdigest()

	def lookup(self, survey_id, include_responses = True, include_questions = True, max_questions = 30, include_project_data = False, include_references = False):
		""" Get summary information of a survey

		Params:
			survey_id (str) - Survey key, found by checking the network request made on the EchoMobile dashboard
		Optional:
			include_responses (boolean)
			include_questions (boolean)
			max_questions (int)
			include_project_data (boolean)
			include_references (boolean)

		Returns:
			resp_ (dict) - Dict with survey attrs
		"""
		to_int = {True: 1, False: 0}
		url = f"/api/cms/survey/{survey_id}?with_response_data={to_int[include_responses]}&with_questions={to_int[include_questions]}&max_questions={max_questions}&with_project={to_int[include_questions]}&with_references={to_int[include_references]}"

		resp = self.requestor.make_request(url, req = "GET")
		
		if(resp == 1):
			resp_ = {}
		else:
			if(resp["message"] == "Target not found, please try again" or resp["message"] == "Survey not found or not accessible"):
				self.logger.error("Survey not found")
				resp_ = {}
			else:
				resp_ = resp["survey"]
		
		return resp_


	def trigger(self, phone, survey_id, name = None):
		""" Send a survey to phone number(s)
		Params:
			phone (str) - The phone number to send to in ISO format. Check first that the contact is available for survey. clients.available_for_survey()
			survey_id (int) - ID of the survey to send. Found under the Survey's summary tab on the dashboard

		Optional:
			name (str) - Name of the contact where we don't already have the contact saved as a client. api.clients.lookup(phone) returns empty

		Returns:
			triggered (bool) - Whether or not the survey has been sent. Logs helpful message too
		"""
		# Check if available for survey first
		cli = Clients(self.requestor, self.logger)
		avail = cli.available_for_survey(phone)

		if(avail):
			url = "/api/v2/trigger/survey"
			digest = self.make_digest(phone, survey_id)

			to_who = {"phone": phone, "digest": digest, "survey_id": survey_id}

			if(name is not None):
				to_who["name"] = name

			res = self.requestor.make_request(url, to_who)

			if(res == 1):
				return False 
			else:
				if(res["success"]):
					return True
				else:
					self.logger.error(res["message"])
					return False
		else:
			self.logger.error("Client is not available for survey.")
			return False

	def list_surveys(self, project_name = None, project_id = None, max_records = 200):
		""" Get a list of all surverys

		Optional:
			project_name (str) - Name of the project the surveys are under
			project_id (int) - 
			max_records (int) - Total records to return. Default is 200 (the max)
		"""
		if(project_name is not None and project_id is not None):
			url = f"/api/cms/survey?project_name={project_name}&project_id={project_id}&max={max_records}"
		else:
			if(project_name is None):
				url = f"/api/cms/survey?project_id={project_id}&max={max_records}"
			elif(project_id is None):
				url = f"/api/cms/survey?max={max_records}"

		resp = self.requestor.make_request(url, req = "GET")

		if(resp == 1):
			surs = [] 
		else:
			if(resp["success"]):
				surs =  resp["surveys"]
			else:
				self.logger.error(res["message"])
				surs = []

		return surs

	def get_survey_responses(self, survey_id, since, until = None, page = None, page_indexing = 0):
		""" Get responses for a specific survey

		Params:
			survey_id (int) - ID of the survey to send. Found under the Survey's summary tab on the dashboard
			since - Unix timestamp to filter since
		Optional:
			until - Unix timestamp to filter till
			page - Page of results to get; for pagination
			page_indexing - Default start page

		Returns:
			resps (list) - A list of clients with their responses (see the attr client_surveys). List is empty if no responses or if error
		"""
		if(until is None):
			until = int(time.time())

		url = "/api/v2/survey_data"

		gt = {"sid": survey_id, "since": since, "until": until, "page_indexing": page_indexing}

		if(page is not None):
			gt["page"] = page
	
		srs = self.requestor.make_request(url, data = gt)

		if(srs == 1):
			resps = []
		else:
			if(srs["success"]):
				pprint.pprint(srs)
				resps = srs["clients"]
			else:
				self.logger.error(srs["message"])
				resps = []

		return resps

