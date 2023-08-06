from ..util import Model


class ActionWrapper(Model):
	def __init__(self):
		self.__custom_views = None
		self.__key_modified = dict()

	def get_custom_views(self):
		"""
		This method gets the custom_views

		Returns:
		List : An instance of List
		"""

		return self.__custom_views

	def set_custom_views(self, custom_views):
		"""
		This method sets the value to custom_views

		Parameters:
		custom_views (List) : An instance of List
		"""

		self.__custom_views = custom_views
		self.__key_modified["custom_views"] = 1

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
