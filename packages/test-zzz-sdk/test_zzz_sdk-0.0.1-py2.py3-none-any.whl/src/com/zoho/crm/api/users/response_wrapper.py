from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__users = None
		self.__key_modified = dict()

	def get_users(self):
		"""
		This method gets the users

		Returns:
		List : An instance of List
		"""

		return self.__users

	def set_users(self, users):
		"""
		This method sets the value to users

		Parameters:
		users (List) : An instance of List
		"""

		self.__users = users
		self.__key_modified["users"] = 1

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
