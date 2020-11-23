class Notice(object):
	def __init__(self, requests_class):
		""" Init Notice object

		Params:
			requests_class (obj) - The util that makes HTTP requests
		"""
		self.requestor = requests_class