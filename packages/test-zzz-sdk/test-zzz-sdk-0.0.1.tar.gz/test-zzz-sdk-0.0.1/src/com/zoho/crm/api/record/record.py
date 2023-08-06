from ..fields import Field
from ..util import Model


class Record(Model):
	def __init__(self):
		self.__id = None
		self.__created_by = None
		self.__created_time = None
		self.__modified_by = None
		self.__modified_time = None
		self.__key_values = dict()
		self.__key_modified = dict()

	def add_field_value(self, field, value):
		"""
		This method is used to add field value

		Parameters:
		field (Field) : An instance of Field
		value (T) : 
		"""

		self.__add_key_value(field.get_api_name(), value)

	def add_key_value(self, api_name, value):
		"""
		This method is used to add key value

		Parameters:
		api_name (string) : A string value
		value (Object) : An instance of Object
		"""

		self.__key_values[api_name] = value

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

	def get_created_by(self):
		"""
		This method gets the created_by

		Returns:
		User : An instance of User
		"""

		return self.__created_by

	def set_created_by(self, created_by):
		"""
		This method sets the value to created_by

		Parameters:
		created_by (User) : An instance of User
		"""

		self.__created_by = created_by
		self.__key_modified["Created_By"] = 1

	def get_created_time(self):
		"""
		This method gets the created_time

		Returns:
		LocalDateTime : An instance of LocalDateTime
		"""

		return self.__created_time

	def set_created_time(self, created_time):
		"""
		This method sets the value to created_time

		Parameters:
		created_time (LocalDateTime) : An instance of LocalDateTime
		"""

		self.__created_time = created_time
		self.__key_modified["Created_Time"] = 1

	def get_modified_by(self):
		"""
		This method gets the modified_by

		Returns:
		User : An instance of User
		"""

		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		This method sets the value to modified_by

		Parameters:
		modified_by (User) : An instance of User
		"""

		self.__modified_by = modified_by
		self.__key_modified["Modified_By"] = 1

	def get_modified_time(self):
		"""
		This method gets the modified_time

		Returns:
		LocalDateTime : An instance of LocalDateTime
		"""

		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		This method sets the value to modified_time

		Parameters:
		modified_time (LocalDateTime) : An instance of LocalDateTime
		"""

		self.__modified_time = modified_time
		self.__key_modified["Modified_Time"] = 1

	def get_key_values(self):
		"""
		This method gets the key_values

		Returns:
		HashMap : An instance of dict
		"""

		return self.__key_values

	def set_key_values(self, key_values):
		"""
		This method sets the value to key_values

		Parameters:
		key_values (dict) : An instance of dict
		"""

		self.__key_values = key_values

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
