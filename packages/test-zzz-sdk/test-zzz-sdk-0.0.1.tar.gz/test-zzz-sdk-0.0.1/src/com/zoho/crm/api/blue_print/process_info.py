from ..util import Model


class ProcessInfo(Model):
	def __init__(self):
		self.__id = None
		self.__field_id = None
		self.__is_continuous = None
		self.__api_name = None
		self.__continuous = None
		self.__field_label = None
		self.__name = None
		self.__column_name = None
		self.__field_value = None
		self.__field_name = None
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

	def get_field_id(self):
		"""
		This method gets the field_id

		Returns:
		Long : A string value
		"""

		return self.__field_id

	def set_field_id(self, field_id):
		"""
		This method sets the value to field_id

		Parameters:
		field_id (string) : A string value
		"""

		self.__field_id = field_id
		self.__key_modified["field_id"] = 1

	def get_is_continuous(self):
		"""
		This method gets the is_continuous

		Returns:
		Boolean : A Boolean value
		"""

		return self.__is_continuous

	def set_is_continuous(self, is_continuous):
		"""
		This method sets the value to is_continuous

		Parameters:
		is_continuous (Boolean) : A Boolean value
		"""

		self.__is_continuous = is_continuous
		self.__key_modified["is_continuous"] = 1

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

	def get_continuous(self):
		"""
		This method gets the continuous

		Returns:
		Boolean : A Boolean value
		"""

		return self.__continuous

	def set_continuous(self, continuous):
		"""
		This method sets the value to continuous

		Parameters:
		continuous (Boolean) : A Boolean value
		"""

		self.__continuous = continuous
		self.__key_modified["continuous"] = 1

	def get_field_label(self):
		"""
		This method gets the field_label

		Returns:
		String : A string value
		"""

		return self.__field_label

	def set_field_label(self, field_label):
		"""
		This method sets the value to field_label

		Parameters:
		field_label (string) : A string value
		"""

		self.__field_label = field_label
		self.__key_modified["field_label"] = 1

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

	def get_column_name(self):
		"""
		This method gets the column_name

		Returns:
		String : A string value
		"""

		return self.__column_name

	def set_column_name(self, column_name):
		"""
		This method sets the value to column_name

		Parameters:
		column_name (string) : A string value
		"""

		self.__column_name = column_name
		self.__key_modified["column_name"] = 1

	def get_field_value(self):
		"""
		This method gets the field_value

		Returns:
		String : A string value
		"""

		return self.__field_value

	def set_field_value(self, field_value):
		"""
		This method sets the value to field_value

		Parameters:
		field_value (string) : A string value
		"""

		self.__field_value = field_value
		self.__key_modified["field_value"] = 1

	def get_field_name(self):
		"""
		This method gets the field_name

		Returns:
		String : A string value
		"""

		return self.__field_name

	def set_field_name(self, field_name):
		"""
		This method sets the value to field_name

		Parameters:
		field_name (string) : A string value
		"""

		self.__field_name = field_name
		self.__key_modified["field_name"] = 1

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
