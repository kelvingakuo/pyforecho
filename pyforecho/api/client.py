class Clients(object):
	def __init__(self, requests_class, logger):
		""" Init Client object

		Params:
			requests_class (obj) - The util that makes HTTP requests
			logger (obj) - A configured object of the 'logging' module
		"""
		self.requestor = requests_class
		self.logger = logger

	def lookup(self, phone, fields = None):
		""" Search for a client using a phone number (in ISO format)

		Params:
			phone (str) - A phone number in the ISO format
			fields (str list) - List of field names to return

		Returns:
			resp_ (dict) - Dict with client attributes. Blank if not registered
		"""
		url = "/api/clients/lookup"
		search = {"phone": phone, "fields": fields}
		resp = self.requestor.make_request(url, search)

		if(resp == 1):
			resp_ = {}
		else:
			if(resp["message"] == "Contact not yet registered"):
				self.logger.error("Contact not yet registered")
				resp_ = {}
			else:
				resp_ = resp["client"]

		return resp_

	def create(self, phone, group_key, name, internal_id = None, location = None, login_code = None, lat = None, lon = None, labels = []):
		""" Add a client to the contact list

		Params:
			phone (str) - A phone number in the ISO format
			group_key (str) - The key for the contact group to create the client in. For a client already in another contact group, they'll be moved to this group. For existing client (found via lookup), this is the attribute 'group_key'. For non-existing clients, it seems that you'd need to look at the network request made when you open the contact group on the EchoMobile dashboard.
			name (str) - The client's name

		Optional:	
			internal_id (int) - For existing clients, this is the field 'eid'
			location (str)
			login_code (str)
			lat (str)
			lon (str)
			labels (str list)

		Returns:
			created (bool) - Whether or not the client has been created. Logs helpful message too
		"""
		
		url = "/api/cms/client"
		new = {
			"phone" : phone, 
			"group_key": group_key
		}
		resp = self.requestor.make_request(url, new)
		
		if(resp == 1):
			return False
		else:
			if(resp["message"] == "Contact updated!"):
				self.logger.info("Existing client updated!")
				return True
			else:
				self.logger.info("Client created!")
				return True
			
	def get_all(self, since, group_name, fields = [], page = 1):
		""" Return a list of all clients in a contact group

		Params:
			since (int) - Return the contacts synced into this group, since this Unix timestamp
			group_name - The name of the contact group as on the EchoMobile dashboard (This is not the group key)

		Optional:
			fields (str list)
			page (int) - For pagination purposes. The first page is 1, and results are paginated at 1000 items

		Returns:
			resp_ (ls) - List of clients in that group. Empty list if none
		"""

		url = "/api/clients/registrations"
		a_ls = {
			"since" : since,
			"group" : group_name,
			"fields": fields,
			"page": page
		}

		resp = self.requestor.make_request(url, a_ls)
		if(resp == 1):
			resp_ = []
		else:
			if(resp["success"]):
				resp_ = resp["clients"]
			else:
				self.logger.error(resp["message"])
				resp_ = []

		return resp_

	def update_client_field(self, client_key, field_key, value):
		""" Update the contents of a custom field for a client
		Params:
			client_key (str) - Unique identifier of the client. Can be found in the field 'key' in the client object returned by lookup() or create() 
			field_key (str) - Unique idntifier of the field whose value to updated
			value (str) - The value to update the field with
		
		Returns:
			updated (bool) - Whether or not the client's field has been updated. Logs helpful message too
		"""
		url = "/api/cms/clientfield"
		updt = {"ckey": client_key, "fkey": field_key, "value": value}

		res = self.requestor.make_request(url, updt)
		
		if(res == 1):
			return False
		else:
			if(res["success"]):
				self.logger.info(res["message"])
				return True
			else:
				self.logger.error(res["message"])
				return False

	def available_for_survey(self, phone):
		""" Utility method to check if a contact is available for survey

		Params:
			phone (str) - Phone number in ISO format

		Returns:
			available (bool) - Whether or not the contact is available for survey
		"""
		cli = self.lookup(phone)

		if(cli == {}):
			self.logger.info("Contact available for survey")
			available = False
		else:
			available = cli["available_for_survey"]
			
		return available


