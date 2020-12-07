import hashlib
import pprint

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
				pass 
			else:
				if(res["success"]):
					self.logger.info(res["message"])
				else:
					self.logger.error(res["message"])
					raise PyForEchoException(res["message"])
		else:
			self.logger.error("Client is not available for survey.")

	def get_all():
		""" Get a list of all surverys
		"""
		pass

	def get_survey_responses():
		""" Get responses for a specific survey
		"""
		pass

