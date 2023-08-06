from ..util import Model


class UpsertBodyWrapper(Model):
	def __init__(self):
		self.__data = None
		self.__key_modified = dict()

	def get_data(self):
		"""
		This method gets the data

		Returns:
		List : An instance of List
		"""

		return self.__data

	def set_data(self, data):
		"""
		This method sets the value to data

		Parameters:
		data (List) : An instance of List
		"""

		self.__data = data
		self.__key_modified["data"] = 1

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
