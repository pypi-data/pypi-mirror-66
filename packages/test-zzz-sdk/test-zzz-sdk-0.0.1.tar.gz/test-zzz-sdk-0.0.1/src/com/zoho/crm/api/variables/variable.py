from ..util import Model


class Variable(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__name = None
		self.__description = None
		self.__type = None
		self.__value = None
		self.__variable_group = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		This method gets the id

		Returns:
		Long : A string value
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

	def get_name(self):
		"""
		This method gets the name

		Returns:
		String : A string value
		"""

		return self.__name

	def set_name(self, name):
		"""
		This method sets the value to name

		Parameters:
		name (string) : A string value
		"""

		self.__name = name
		self.__key_modified["name"] = 1

	def get_description(self):
		"""
		This method gets the description

		Returns:
		String : A string value
		"""

		return self.__description

	def set_description(self, description):
		"""
		This method sets the value to description

		Parameters:
		description (string) : A string value
		"""

		self.__description = description
		self.__key_modified["description"] = 1

	def get_type(self):
		"""
		This method gets the type

		Returns:
		String : A string value
		"""

		return self.__type

	def set_type(self, type):
		"""
		This method sets the value to type

		Parameters:
		type (string) : A string value
		"""

		self.__type = type
		self.__key_modified["type"] = 1

	def get_value(self):
		"""
		This method gets the value

		Returns:
		String : A string value
		"""

		return self.__value

	def set_value(self, value):
		"""
		This method sets the value to value

		Parameters:
		value (string) : A string value
		"""

		self.__value = value
		self.__key_modified["value"] = 1

	def get_variable_group(self):
		"""
		This method gets the variable_group

		Returns:
		VariableGroup : An instance of VariableGroup
		"""

		return self.__variable_group

	def set_variable_group(self, variable_group):
		"""
		This method sets the value to variable_group

		Parameters:
		variable_group (VariableGroup) : An instance of VariableGroup
		"""

		self.__variable_group = variable_group
		self.__key_modified["variable_group"] = 1

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
