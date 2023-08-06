from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__fields = None
		self.__key_modified = dict()

	def get_fields(self):
		"""
		This method gets the fields

		Returns:
		List : An instance of List
		"""

		return self.__fields

	def set_fields(self, fields):
		"""
		This method sets the value to fields

		Parameters:
		fields (List) : An instance of List
		"""

		self.__fields = fields
		self.__key_modified["fields"] = 1

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
