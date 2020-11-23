from os import path, remove

import json
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ================ Logger
if path.isfile("logs/logs.log"):
    remove("logs/logs.log")
# Create the Logger
logger = logging.getLogger('meGlobalLogger')
logger.setLevel(logging.DEBUG)
console_logger = logging.StreamHandler()
format = logging.Formatter('%(levelname)s : %(asctime)-15s : %(message)s', '%d/%m/%Y %I:%M:%S %p')
console_logger.setFormatter(format)
logger.addHandler(console_logger)


# ================ HTTP Request
class MakeRequests(object):
	def __init__(self, headers):
		self.headers = headers
		retries = Retry(total = 10, backoff_factor = 2, status_forcelist = [500, 502, 503, 504, 404])
		self.sess = requests.Session()
		self.sess.mount("https://", HTTPAdapter(max_retries = retries))
		self.timeout = 10

	def make_request(self, endpoint, data):
		""" Helper for HTTP requests

		Params:
			endpoint (str) - The endpoint to call (without the domain portion)
			headers (dict) - The auth headers
			data (dict) - The data to put in the request

		Returns:
			If an error occurs, the error message is printed, then 1 returned
			If no error occurs, returns the response as dict
		"""
		target = f"https://www.echomobile.io{endpoint}"

		try:
			resp = self.sess.post(target,
					data = data,
					headers = self.headers,
					timeout = self.timeout
				)

			if(resp.status_code != 200):
				logger.error("ERROR!")
				logger.error(f"Status code: {resp.status_code}")
				logger.error(f"{json.loads(resp.text)['message']}")
				return 1
			else:
				return json.loads(resp.text)
		except Exception as e:
			logger.error("An error occured")
			logger.error(e)
			