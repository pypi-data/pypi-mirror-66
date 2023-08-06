from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__org = None
		self.__key_modified = dict()

	def get_org(self):
		"""
		This method gets the org

		Returns:
		List : An instance of List
		"""

		return self.__org

	def set_org(self, org):
		"""
		This method sets the value to org

		Parameters:
		org (List) : An instance of List
		"""

		self.__org = org
		self.__key_modified["org"] = 1

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
