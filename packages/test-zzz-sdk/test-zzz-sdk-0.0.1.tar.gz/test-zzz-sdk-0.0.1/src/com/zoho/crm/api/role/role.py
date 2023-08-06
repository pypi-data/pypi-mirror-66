from ..util import Model


class Role(Model):
	def __init__(self):
		self.__id = None
		self.__name = None
		self.__display_label = None
		self.__admin_user = None
		self.__reporting_to = None
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

	def get_admin_user(self):
		"""
		This method gets the admin_user

		Returns:
		Boolean : A Boolean value
		"""

		return self.__admin_user

	def set_admin_user(self, admin_user):
		"""
		This method sets the value to admin_user

		Parameters:
		admin_user (Boolean) : A Boolean value
		"""

		self.__admin_user = admin_user
		self.__key_modified["admin_user"] = 1

	def get_reporting_to(self):
		"""
		This method gets the reporting_to

		Returns:
		User : An instance of User
		"""

		return self.__reporting_to

	def set_reporting_to(self, reporting_to):
		"""
		This method sets the value to reporting_to

		Parameters:
		reporting_to (User) : An instance of User
		"""

		self.__reporting_to = reporting_to
		self.__key_modified["reporting_to"] = 1

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
