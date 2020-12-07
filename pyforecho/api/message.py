import hashlib

class Messages(object):
	def __init__(self, requests_class, logger):
		""" Init Message object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger
		self.md5_pw = "a812801c81bdf2"

	def make_digest(self, phone, message):
		dig_ = ''.join([self.md5_pw, phone, message])
		dig = dig_.encode()
		m = hashlib.md5(dig)
		return m.hexdigest()

	def send_message(self, phone, message, name = None):
		""" Send bulk message(s) to phone number(s)

		Params:
			phone (str) - Contact's phone number in the ISO format
			message (str) - The message to send the contact
			
		Optional:
			name (str) - Name of the contact where we don't already have the contact saved as a client. api.clients.lookup(phone) returns empty

		Returns:
			queued (bool) - Whether or not the message has been successfully queued for sending. Logs helpful message too
		"""
		url = "/api/messaging/send"
		dig = self.make_digest(phone, message)
		msg = {"phone": phone, "message": message, "digest": dig}

		if(name is not None):
			msg["name"] = name

		resp = self.requestor.make_request(url, msg)
		
		if(resp == 1):
			return False 
		else:
			if(resp["success"]):
				self.logger.info(resp["message"])
				return True
			else:
				self.logger.error(resp["message"])
				return False