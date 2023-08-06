from ..util import Model


class ConvertResponse(Model):
	def __init__(self):
		self.__contacts = None
		self.__deals = None
		self.__accounts = None
		self.__key_modified = dict()

	def get_contacts(self):
		"""
		This method gets the contacts

		Returns:
		Long : A string value
		"""

		return self.__contacts

	def set_contacts(self, contacts):
		"""
		This method sets the value to contacts

		Parameters:
		contacts (string) : A string value
		"""

		self.__contacts = contacts
		self.__key_modified["Contacts"] = 1

	def get_deals(self):
		"""
		This method gets the deals

		Returns:
		Long : A string value
		"""

		return self.__deals

	def set_deals(self, deals):
		"""
		This method sets the value to deals

		Parameters:
		deals (string) : A string value
		"""

		self.__deals = deals
		self.__key_modified["Deals"] = 1

	def get_accounts(self):
		"""
		This method gets the accounts

		Returns:
		Long : A string value
		"""

		return self.__accounts

	def set_accounts(self, accounts):
		"""
		This method sets the value to accounts

		Parameters:
		accounts (string) : A string value
		"""

		self.__accounts = accounts
		self.__key_modified["Accounts"] = 1

	def is_key_modified(self, key):
		"""
		This method is used to check if the user has modified the given key

		Parameters:
		key (string) : A string value

		Returns:
		Integer : A int value
		"""

		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		"""
		This method is used to mark the given key as modified

		Parameters:
		modification (int) : A int value
		key (string) : A string value
		"""

		self.__key_modified[key] = modification
