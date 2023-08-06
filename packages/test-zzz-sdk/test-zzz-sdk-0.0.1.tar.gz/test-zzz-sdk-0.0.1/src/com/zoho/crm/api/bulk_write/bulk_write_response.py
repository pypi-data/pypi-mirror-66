from ..util import Model


class BulkWriteResponse(Model):
	def __init__(self):
		self.__status = None
		self.__character_encoding = None
		self.__resource = None
		self.__id = None
		self.__result = None
		self.__operation = None
		self.__created_time = None
		self.__key_modified = dict()

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

	def get_character_encoding(self):
		"""
		This method gets the character_encoding

		Returns:
		String : A string value
		"""

		return self.__character_encoding

	def set_character_encoding(self, character_encoding):
		"""
		This method sets the value to character_encoding

		Parameters:
		character_encoding (string) : A string value
		"""

		self.__character_encoding = character_encoding
		self.__key_modified["character_encoding"] = 1

	def get_resource(self):
		"""
		This method gets the resource

		Returns:
		Resource : An instance of Resource
		"""

		return self.__resource

	def set_resource(self, resource):
		"""
		This method sets the value to resource

		Parameters:
		resource (Resource) : An instance of Resource
		"""

		self.__resource = resource
		self.__key_modified["resource"] = 1

	def get_id(self):
		"""
		This method gets the id

		Returns:
		Integer : A int value
		"""

		return self.__id

	def set_id(self, id):
		"""
		This method sets the value to id

		Parameters:
		id (int) : A int value
		"""

		self.__id = id
		self.__key_modified["id"] = 1

	def get_result(self):
		"""
		This method gets the result

		Returns:
		Map : An instance of Map
		"""

		return self.__result

	def set_result(self, result):
		"""
		This method sets the value to result

		Parameters:
		result (Map) : An instance of Map
		"""

		self.__result = result
		self.__key_modified["result"] = 1

	def get_operation(self):
		"""
		This method gets the operation

		Returns:
		String : A string value
		"""

		return self.__operation

	def set_operation(self, operation):
		"""
		This method sets the value to operation

		Parameters:
		operation (string) : A string value
		"""

		self.__operation = operation
		self.__key_modified["operation"] = 1

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
		self.__key_modified["created_time"] = 1

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
