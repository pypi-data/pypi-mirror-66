from ..util import Model


class Field(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__data_type = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		This method gets the id

		Returns:
		String : A string value
		"""

		return self.__id

	def set_id(self, id):
		"""
		This method sets the value to id

		Parameters:
		id (string) : A string value
		"""

		self.__id = id
		self.__key_modified["id"] = 1

	def get_api_name(self):
		"""
		This method gets the api_name

		Returns:
		String : A string value
		"""

		return self.__api_name

	def set_api_name(self, api_name):
		"""
		This method sets the value to api_name

		Parameters:
		api_name (string) : A string value
		"""

		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_data_type(self):
		"""
		This method gets the data_type

		Returns:
		String : A string value
		"""

		return self.__data_type

	def set_data_type(self, data_type):
		"""
		This method sets the value to data_type

		Parameters:
		data_type (string) : A string value
		"""

		self.__data_type = data_type
		self.__key_modified["data_type"] = 1

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
