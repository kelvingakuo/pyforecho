class Project(object):
	def __init__(self, requests_class):
		""" Init Project object

		Params:
			requests_class (obj) - The util that makes HTTP requests
		"""
		self.requestor = requests_class