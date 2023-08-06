from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__related_lists = None
		self.__key_modified = dict()

	def get_related_lists(self):
		"""
		This method gets the related_lists

		Returns:
		List : An instance of List
		"""

		return self.__related_lists

	def set_related_lists(self, related_lists):
		"""
		This method sets the value to related_lists

		Parameters:
		related_lists (List) : An instance of List
		"""

		self.__related_lists = related_lists
		self.__key_modified["related_lists"] = 1

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
