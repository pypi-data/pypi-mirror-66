from ..util import Model


class MergeWrapper(Model):
	def __init__(self):
		self.__tags = None
		self.__key_modified = dict()

	def get_tags(self):
		"""
		This method gets the tags

		Returns:
		List : An instance of List
		"""

		return self.__tags

	def set_tags(self, tags):
		"""
		This method sets the value to tags

		Parameters:
		tags (List) : An instance of List
		"""

		self.__tags = tags
		self.__key_modified["tags"] = 1

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
