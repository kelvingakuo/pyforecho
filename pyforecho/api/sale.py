class Sale(object):
	def __init__(self, requests_class):
		""" Init Sale object

		Params:
			requests_class (obj) - The util that makes HTTP requests
		"""
		self.requestor = requests_class