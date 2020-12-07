import time
import pprint

class Inbox(object):
	def __init__(self, requests_class, logger):
		""" Init Inbox object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger

	def list_messages(self, since, until = None, starred = False, archived = False, unread = False, page = 1, max_records = 200):
		""" List messages in the inbox

		Params:
			since - Unix timestamp to extract since

		Optional:
			until - Unix timestamp to extract until. Default is now
			starred - 'True' to return starred messages only
			archived - 'True' to return archived messages only
			unread - 'True' to return unread messages only
			page - The page to get. Items are paginated at 200 per page
			max_records - Total records to get. Default is 200 (the max)

		Returns:
		msgs - List of message dicts and their attributes. Empty list if error or no data

		"""
		if(until is None):
			until = int(time.time())

		to_int = {True: 1, False: 0}

		url = f"/api/cms/inbox?starred (optional)={to_int[starred]}&archived (optional)={to_int[archived]}&unread (optional)={to_int[unread]}&since (optional)={since}&until (optional)={until}&page (optional)={page}&max(optional)={max_records}"
		resp = self.requestor.make_request(url, req = "GET")

		if(resp == 1):
			msgs = []
		else:
			if(resp["success"]):
				self.logger.info("Messages available")
				msgs = resp["ims"]
			else:
				self.logger.error("An error occured")
				msgs = []

		return msgs