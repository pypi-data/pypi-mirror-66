from ..util import Model


class Module(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__module_name = None
		self.__convertable = None
		self.__editable = None
		self.__deletable = None
		self.__web_link = None
		self.__singular_label = None
		self.__modified_time = None
		self.__viewable = None
		self.__api_supported = None
		self.__createable = None
		self.__plural_label = None
		self.__generated_type = None
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

	def get_api_name(self):
		"""
		This method gets the api_name

		Returns:
		String : A string value
		"""

		return self.__api_name

	def set_api_name(self, api_name):
		"""
		This method sets the value to api_name

		Parameters:
		api_name (string) : A string value
		"""

		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_module_name(self):
		"""
		This method gets the module_name

		Returns:
		String : A string value
		"""

		return self.__module_name

	def set_module_name(self, module_name):
		"""
		This method sets the value to module_name

		Parameters:
		module_name (string) : A string value
		"""

		self.__module_name = module_name
		self.__key_modified["module_name"] = 1

	def get_convertable(self):
		"""
		This method gets the convertable

		Returns:
		Boolean : A Boolean value
		"""

		return self.__convertable

	def set_convertable(self, convertable):
		"""
		This method sets the value to convertable

		Parameters:
		convertable (Boolean) : A Boolean value
		"""

		self.__convertable = convertable
		self.__key_modified["convertable"] = 1

	def get_editable(self):
		"""
		This method gets the editable

		Returns:
		Boolean : A Boolean value
		"""

		return self.__editable

	def set_editable(self, editable):
		"""
		This method sets the value to editable

		Parameters:
		editable (Boolean) : A Boolean value
		"""

		self.__editable = editable
		self.__key_modified["editable"] = 1

	def get_deletable(self):
		"""
		This method gets the deletable

		Returns:
		Boolean : A Boolean value
		"""

		return self.__deletable

	def set_deletable(self, deletable):
		"""
		This method sets the value to deletable

		Parameters:
		deletable (Boolean) : A Boolean value
		"""

		self.__deletable = deletable
		self.__key_modified["deletable"] = 1

	def get_web_link(self):
		"""
		This method gets the web_link

		Returns:
		String : A string value
		"""

		return self.__web_link

	def set_web_link(self, web_link):
		"""
		This method sets the value to web_link

		Parameters:
		web_link (string) : A string value
		"""

		self.__web_link = web_link
		self.__key_modified["web_link"] = 1

	def get_singular_label(self):
		"""
		This method gets the singular_label

		Returns:
		String : A string value
		"""

		return self.__singular_label

	def set_singular_label(self, singular_label):
		"""
		This method sets the value to singular_label

		Parameters:
		singular_label (string) : A string value
		"""

		self.__singular_label = singular_label
		self.__key_modified["singular_label"] = 1

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
		self.__key_modified["modified_time"] = 1

	def get_viewable(self):
		"""
		This method gets the viewable

		Returns:
		Boolean : A Boolean value
		"""

		return self.__viewable

	def set_viewable(self, viewable):
		"""
		This method sets the value to viewable

		Parameters:
		viewable (Boolean) : A Boolean value
		"""

		self.__viewable = viewable
		self.__key_modified["viewable"] = 1

	def get_api_supported(self):
		"""
		This method gets the api_supported

		Returns:
		Boolean : A Boolean value
		"""

		return self.__api_supported

	def set_api_supported(self, api_supported):
		"""
		This method sets the value to api_supported

		Parameters:
		api_supported (Boolean) : A Boolean value
		"""

		self.__api_supported = api_supported
		self.__key_modified["api_supported"] = 1

	def get_createable(self):
		"""
		This method gets the createable

		Returns:
		Boolean : A Boolean value
		"""

		return self.__createable

	def set_createable(self, createable):
		"""
		This method sets the value to createable

		Parameters:
		createable (Boolean) : A Boolean value
		"""

		self.__createable = createable
		self.__key_modified["createable"] = 1

	def get_plural_label(self):
		"""
		This method gets the plural_label

		Returns:
		String : A string value
		"""

		return self.__plural_label

	def set_plural_label(self, plural_label):
		"""
		This method sets the value to plural_label

		Parameters:
		plural_label (string) : A string value
		"""

		self.__plural_label = plural_label
		self.__key_modified["plural_label"] = 1

	def get_generated_type(self):
		"""
		This method gets the generated_type

		Returns:
		String : A string value
		"""

		return self.__generated_type

	def set_generated_type(self, generated_type):
		"""
		This method sets the value to generated_type

		Parameters:
		generated_type (string) : A string value
		"""

		self.__generated_type = generated_type
		self.__key_modified["generated_type"] = 1

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
		self.__key_modified["modified_by"] = 1

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
