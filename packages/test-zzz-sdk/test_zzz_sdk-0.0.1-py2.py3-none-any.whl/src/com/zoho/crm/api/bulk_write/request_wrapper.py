from ..util import Model


class RequestWrapper(Model):
	def __init__(self):
		self.__character_encoding = None
		self.__operation = None
		self.__callback = None
		self.__resource = None
		self.__key_modified = dict()

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

	def get_callback(self):
		"""
		This method gets the callback

		Returns:
		CallBack : An instance of CallBack
		"""

		return self.__callback

	def set_callback(self, callback):
		"""
		This method sets the value to callback

		Parameters:
		callback (CallBack) : An instance of CallBack
		"""

		self.__callback = callback
		self.__key_modified["callback"] = 1

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
