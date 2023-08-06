from ..util import Model


class Resource(Model):
	def __init__(self):
		self.__type = None
		self.__module = None
		self.__file_id = None
		self.__ignore_empty = None
		self.__find_by = None
		self.__field_mappings = None
		self.__file = None
		self.__key_modified = dict()

	def get_type(self):
		"""
		This method gets the type

		Returns:
		String : A string value
		"""

		return self.__type

	def set_type(self, type):
		"""
		This method sets the value to type

		Parameters:
		type (string) : A string value
		"""

		self.__type = type
		self.__key_modified["type"] = 1

	def get_module(self):
		"""
		This method gets the module

		Returns:
		String : A string value
		"""

		return self.__module

	def set_module(self, module):
		"""
		This method sets the value to module

		Parameters:
		module (string) : A string value
		"""

		self.__module = module
		self.__key_modified["module"] = 1

	def get_file_id(self):
		"""
		This method gets the file_id

		Returns:
		String : A string value
		"""

		return self.__file_id

	def set_file_id(self, file_id):
		"""
		This method sets the value to file_id

		Parameters:
		file_id (string) : A string value
		"""

		self.__file_id = file_id
		self.__key_modified["file_id"] = 1

	def get_ignore_empty(self):
		"""
		This method gets the ignore_empty

		Returns:
		Boolean : A Boolean value
		"""

		return self.__ignore_empty

	def set_ignore_empty(self, ignore_empty):
		"""
		This method sets the value to ignore_empty

		Parameters:
		ignore_empty (Boolean) : A Boolean value
		"""

		self.__ignore_empty = ignore_empty
		self.__key_modified["ignore_empty"] = 1

	def get_find_by(self):
		"""
		This method gets the find_by

		Returns:
		String : A string value
		"""

		return self.__find_by

	def set_find_by(self, find_by):
		"""
		This method sets the value to find_by

		Parameters:
		find_by (string) : A string value
		"""

		self.__find_by = find_by
		self.__key_modified["find_by"] = 1

	def get_field_mappings(self):
		"""
		This method gets the field_mappings

		Returns:
		List : An instance of List
		"""

		return self.__field_mappings

	def set_field_mappings(self, field_mappings):
		"""
		This method sets the value to field_mappings

		Parameters:
		field_mappings (List) : An instance of List
		"""

		self.__field_mappings = field_mappings
		self.__key_modified["field_mappings"] = 1

	def get_file(self):
		"""
		This method gets the file

		Returns:
		File : An instance of File
		"""

		return self.__file

	def set_file(self, file):
		"""
		This method sets the value to file

		Parameters:
		file (File) : An instance of File
		"""

		self.__file = file
		self.__key_modified["file"] = 1

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
