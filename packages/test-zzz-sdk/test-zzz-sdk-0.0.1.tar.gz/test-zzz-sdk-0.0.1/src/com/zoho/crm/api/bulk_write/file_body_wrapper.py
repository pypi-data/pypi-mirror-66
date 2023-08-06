
from ..util import Model


class FileBodyWrapper(Model):
	def __init__(self):
		self.__file = None
		self.__key_modified = dict()

	def get_file(self):
		"""
		This method gets the file

		Returns:
		StreamWrapper : An instance of StreamWrapper
		"""

		return self.__file

	def set_file(self, file):
		"""
		This method sets the value to file

		Parameters:
		file (StreamWrapper) : An instance of StreamWrapper
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
