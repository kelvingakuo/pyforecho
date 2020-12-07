# -*- coding: utf-8 -*-
import sys
if(sys.version_info <= (2,7)):
	sys.exit("Sorry. This package doesn't support Python 2.7 or prior. v3.6 and above preferred")

import json
import pprint
import time

from .utils import MakeRequests
from .utils import logger

from .api import account
from .api import activity_log
from .api import client
from .api import entity
from .api import field
from .api import inbox
from .api import message
from .api import msg_log
from .api import notice
from .api import payment
from .api import product
from .api import report
from .api import sale
from .api import serial
from .api import survey
from .api import transaction


class EchoMobile(object):
	def __init__(self, acc_id, eid = None, e_passw = None, user_name = None, user_pass = None):
		"""	Intialise with authentication fields (https://echomobile.io/docs/authentication)

		You have to provide auth info for either 'Enterprise' or 'Account'.

		Params:
			acc_id (int) - Account ID
			eid (int) - Enterprise ID for auth of type 'Enterprise'
			e_passw (str) - Enterprise password for auth of type 'Enterprise'
			user_name (str) - Username for auth of type 'Account'
			user_pass (str) - Password for auth of type 'Account'

		"""

		if(eid == None and e_passw == None and user_name == None and user_pass == None):
			print("You need to provide auth information for either 'Enterprise' or 'Account'")
		elif((eid != None and e_passw == None) or (e_passw != None and eid == None)):
			print("For 'Enterprise' auth, you need to provide both eid and password. For more, visit (https://echomobile.io/docs/authentication)")
		elif((user_name != None and user_pass == None) or (user_name == None and user_pass != None)):
			print("For 'Account' auth, you need to provide both user_name and user_pass. For more,  visit (https://echomobile.io/docs/authentication)")
		elif(eid != None and e_passw != None and user_name != None and user_pass != None):
			print("Provide eid and passw only OR user_name and user_pass only, not both sets")
		else:
			self.acc_id = str(acc_id) if type(acc_id) == int else acc_id

			if(eid != None):
				# Assume it's 'Enterprise'
				self.eid = str(eid) if type(eid) == int else eid
				self.passw = e_passw
			elif(user_pass != None):
				# Assume it's 'Account'
				self.eid = user_name
				self.passw = user_pass

			self.reqs_class = MakeRequests(self.eid, self.passw, self.acc_id)

			self.clients = client.Clients(self.reqs_class, logger)
			self.surveys = survey.Surveys(self.reqs_class, logger)
			self.bulk_messages = message.Messages(self.reqs_class, logger)

	def test_connection(self):
		""" Run this to check if authentication with EchoMobile was successful
		"""
		res = self.clients.lookup("254712345678")
		if(res != 1):
			logger.info("Successful connection.")