from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__variables = None
		self.__key_modified = dict()

	def get_variables(self):
		"""
		This method gets the variables

		Returns:
		List : An instance of List
		"""

		return self.__variables

	def set_variables(self, variables):
		"""
		This method sets the value to variables

		Parameters:
		variables (List) : An instance of List
		"""

		self.__variables = variables
		self.__key_modified["variables"] = 1

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
