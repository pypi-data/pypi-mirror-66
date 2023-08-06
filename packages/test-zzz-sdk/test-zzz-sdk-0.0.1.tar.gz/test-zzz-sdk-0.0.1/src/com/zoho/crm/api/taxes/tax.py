from ..util import Model


class Tax(Model):
	def __init__(self):
		self.__id = None
		self.__value = None
		self.__display_label = None
		self.__name = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		This method gets the id

		Returns:
		String : A string value
		"""

		return self.__id

	def set_id(self, id):
		"""
		This method sets the value to id

		Parameters:
		id (string) : A string value
		"""

		self.__id = id
		self.__key_modified["id"] = 1

	def get_value(self):
		"""
		This method gets the value

		Returns:
		Integer : A int value
		"""

		return self.__value

	def set_value(self, value):
		"""
		This method sets the value to value

		Parameters:
		value (int) : A int value
		"""

		self.__value = value
		self.__key_modified["value"] = 1

	def get_display_label(self):
		"""
		This method gets the display_label

		Returns:
		String : A string value
		"""

		return self.__display_label

	def set_display_label(self, display_label):
		"""
		This method sets the value to display_label

		Parameters:
		display_label (string) : A string value
		"""

		self.__display_label = display_label
		self.__key_modified["display_label"] = 1

	def get_name(self):
		"""
		This method gets the name

		Returns:
		String : A string value
		"""

		return self.__name

	def set_name(self, name):
		"""
		This method sets the value to name

		Parameters:
		name (string) : A string value
		"""

		self.__name = name
		self.__key_modified["name"] = 1

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
