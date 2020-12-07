class Notices(object):
	def __init__(self, requests_class, logger):
		""" Init Notices object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger