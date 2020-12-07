class Inbox(object):
	def __init__(self, requests_class, logger):
		""" Init Inbox object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger

	def list_messages(self):
		""" List inbox messages
		"""
# to_int = {True: 1, False: 0}
# url = f"/api/cms/survey/{survey_id}?with_response_data={to_int[include_responses]}&with_questions={to_int[include_questions]}&max_questions={max_questions}&with_project={to_int[include_questions]}&with_references={to_int[include_references]}"

# resp = self.requestor.make_request(url, req = "GET")

		url = f"/api/cms/inbox"
		resp = self.requestor.make_request(url, req = "GET")