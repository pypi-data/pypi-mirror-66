from ..util import Model


class RecordNotInProgressException(Model):
	def __init__(self):
		self.__code = None
		self.__message = None
		self.__status = None
		self.__details = None
		self.__key_modified = dict()

	def get_code(self):
		"""
		This method gets the code

		Returns:
		String : A string value
		"""

		return self.__code

	def set_code(self, code):
		"""
		This method sets the value to code

		Parameters:
		code (string) : A string value
		"""

		self.__code = code
		self.__key_modified["code"] = 1

	def get_message(self):
		"""
		This method gets the message

		Returns:
		String : A string value
		"""

		return self.__message

	def set_message(self, message):
		"""
		This method sets the value to message

		Parameters:
		message (string) : A string value
		"""

		self.__message = message
		self.__key_modified["message"] = 1

	def get_status(self):
		"""
		This method gets the status

		Returns:
		String : A string value
		"""

		return self.__status

	def set_status(self, status):
		"""
		This method sets the value to status

		Parameters:
		status (string) : A string value
		"""

		self.__status = status
		self.__key_modified["status"] = 1

	def get_details(self):
		"""
		This method gets the details

		Returns:
		Map : An instance of Map
		"""

		return self.__details

	def set_details(self, details):
		"""
		This method sets the value to details

		Parameters:
		details (Map) : An instance of Map
		"""

		self.__details = details
		self.__key_modified["details"] = 1

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
