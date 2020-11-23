class Client(object):
	def __init__(self, requests_class):
		""" Init Client object

		Params:
			requests_class (obj) - The util that makes HTTP requests
		"""
		self.requestor = requests_class