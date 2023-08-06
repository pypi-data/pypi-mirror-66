from ..util import Model


class Note(Model):
	def __init__(self):
		self.__id = None
		self.__note_title = None
		self.__note_content = None
		self.__modified_time = None
		self.__created_time = None
		self.__parent_id = None
		self.__owner = None
		self.__created_by = None
		self.__modified_by = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		This method gets the id

		Returns:
		Long : A string value
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

	def get_note_title(self):
		"""
		This method gets the note_title

		Returns:
		String : A string value
		"""

		return self.__note_title

	def set_note_title(self, note_title):
		"""
		This method sets the value to note_title

		Parameters:
		note_title (string) : A string value
		"""

		self.__note_title = note_title
		self.__key_modified["Note_Title"] = 1

	def get_note_content(self):
		"""
		This method gets the note_content

		Returns:
		String : A string value
		"""

		return self.__note_content

	def set_note_content(self, note_content):
		"""
		This method sets the value to note_content

		Parameters:
		note_content (string) : A string value
		"""

		self.__note_content = note_content
		self.__key_modified["Note_Content"] = 1

	def get_modified_time(self):
		"""
		This method gets the modified_time

		Returns:
		LocalDateTime : An instance of LocalDateTime
		"""

		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		This method sets the value to modified_time

		Parameters:
		modified_time (LocalDateTime) : An instance of LocalDateTime
		"""

		self.__modified_time = modified_time
		self.__key_modified["Modified_Time"] = 1

	def get_created_time(self):
		"""
		This method gets the created_time

		Returns:
		LocalDateTime : An instance of LocalDateTime
		"""

		return self.__created_time

	def set_created_time(self, created_time):
		"""
		This method sets the value to created_time

		Parameters:
		created_time (LocalDateTime) : An instance of LocalDateTime
		"""

		self.__created_time = created_time
		self.__key_modified["Created_Time"] = 1

	def get_parent_id(self):
		"""
		This method gets the parent_id

		Returns:
		Map : An instance of Map
		"""

		return self.__parent_id

	def set_parent_id(self, parent_id):
		"""
		This method sets the value to parent_id

		Parameters:
		parent_id (Map) : An instance of Map
		"""

		self.__parent_id = parent_id
		self.__key_modified["Parent_Id"] = 1

	def get_owner(self):
		"""
		This method gets the owner

		Returns:
		User : An instance of User
		"""

		return self.__owner

	def set_owner(self, owner):
		"""
		This method sets the value to owner

		Parameters:
		owner (User) : An instance of User
		"""

		self.__owner = owner
		self.__key_modified["Owner"] = 1

	def get_created_by(self):
		"""
		This method gets the created_by

		Returns:
		User : An instance of User
		"""

		return self.__created_by

	def set_created_by(self, created_by):
		"""
		This method sets the value to created_by

		Parameters:
		created_by (User) : An instance of User
		"""

		self.__created_by = created_by
		self.__key_modified["Created_By"] = 1

	def get_modified_by(self):
		"""
		This method gets the modified_by

		Returns:
		User : An instance of User
		"""

		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		This method sets the value to modified_by

		Parameters:
		modified_by (User) : An instance of User
		"""

		self.__modified_by = modified_by
		self.__key_modified["Modified_By"] = 1

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
