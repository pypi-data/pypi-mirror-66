from ..util import Model


class Layout(Model):
	def __init__(self):
		self.__view = None
		self.__edit = None
		self.__create = None
		self.__quick_create = None
		self.__key_modified = dict()

	def get_view(self):
		"""
		This method gets the view

		Returns:
		Boolean : A Boolean value
		"""

		return self.__view

	def set_view(self, view):
		"""
		This method sets the value to view

		Parameters:
		view (Boolean) : A Boolean value
		"""

		self.__view = view
		self.__key_modified["view"] = 1

	def get_edit(self):
		"""
		This method gets the edit

		Returns:
		Boolean : A Boolean value
		"""

		return self.__edit

	def set_edit(self, edit):
		"""
		This method sets the value to edit

		Parameters:
		edit (Boolean) : A Boolean value
		"""

		self.__edit = edit
		self.__key_modified["edit"] = 1

	def get_create(self):
		"""
		This method gets the create

		Returns:
		Boolean : A Boolean value
		"""

		return self.__create

	def set_create(self, create):
		"""
		This method sets the value to create

		Parameters:
		create (Boolean) : A Boolean value
		"""

		self.__create = create
		self.__key_modified["create"] = 1

	def get_quick_create(self):
		"""
		This method gets the quick_create

		Returns:
		Boolean : A Boolean value
		"""

		return self.__quick_create

	def set_quick_create(self, quick_create):
		"""
		This method sets the value to quick_create

		Parameters:
		quick_create (Boolean) : A Boolean value
		"""

		self.__quick_create = quick_create
		self.__key_modified["quick_create"] = 1

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
