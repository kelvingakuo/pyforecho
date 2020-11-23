class Survey(object):
	def __init__(self, requests_class, logger):
		""" Init Survey object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger

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


	def trigger():
		""" Send a survey to phone number(s)
		"""
		pass

	def get_all():
		""" Get a list of all surverys
		"""
		pass

	def get_survey_responses():
		""" Get responses for a specific survey
		"""
		pass

