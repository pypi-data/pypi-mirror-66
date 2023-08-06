from ..util import Model


class Transition(Model):
	def __init__(self):
		self.__id = None
		self.__next_transitions = None
		self.__data = None
		self.__next_field_value = None
		self.__name = None
		self.__criteria_matched = None
		self.__fields = None
		self.__criteria_message = None
		self.__percent_partial_save = None
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

	def get_next_transitions(self):
		"""
		This method gets the next_transitions

		Returns:
		List : An instance of List
		"""

		return self.__next_transitions

	def set_next_transitions(self, next_transitions):
		"""
		This method sets the value to next_transitions

		Parameters:
		next_transitions (List) : An instance of List
		"""

		self.__next_transitions = next_transitions
		self.__key_modified["next_transitions"] = 1

	def get_data(self):
		"""
		This method gets the data

		Returns:
		Record : An instance of Record
		"""

		return self.__data

	def set_data(self, data):
		"""
		This method sets the value to data

		Parameters:
		data (Record) : An instance of Record
		"""

		self.__data = data
		self.__key_modified["data"] = 1

	def get_next_field_value(self):
		"""
		This method gets the next_field_value

		Returns:
		String : A string value
		"""

		return self.__next_field_value

	def set_next_field_value(self, next_field_value):
		"""
		This method sets the value to next_field_value

		Parameters:
		next_field_value (string) : A string value
		"""

		self.__next_field_value = next_field_value
		self.__key_modified["next_field_value"] = 1

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

	def get_criteria_matched(self):
		"""
		This method gets the criteria_matched

		Returns:
		Boolean : A Boolean value
		"""

		return self.__criteria_matched

	def set_criteria_matched(self, criteria_matched):
		"""
		This method sets the value to criteria_matched

		Parameters:
		criteria_matched (Boolean) : A Boolean value
		"""

		self.__criteria_matched = criteria_matched
		self.__key_modified["criteria_matched"] = 1

	def get_fields(self):
		"""
		This method gets the fields

		Returns:
		List : An instance of List
		"""

		return self.__fields

	def set_fields(self, fields):
		"""
		This method sets the value to fields

		Parameters:
		fields (List) : An instance of List
		"""

		self.__fields = fields
		self.__key_modified["fields"] = 1

	def get_criteria_message(self):
		"""
		This method gets the criteria_message

		Returns:
		String : A string value
		"""

		return self.__criteria_message

	def set_criteria_message(self, criteria_message):
		"""
		This method sets the value to criteria_message

		Parameters:
		criteria_message (string) : A string value
		"""

		self.__criteria_message = criteria_message
		self.__key_modified["criteria_message"] = 1

	def get_percent_partial_save(self):
		"""
		This method gets the percent_partial_save

		Returns:
		Integer : A int value
		"""

		return self.__percent_partial_save

	def set_percent_partial_save(self, percent_partial_save):
		"""
		This method sets the value to percent_partial_save

		Parameters:
		percent_partial_save (int) : A int value
		"""

		self.__percent_partial_save = percent_partial_save
		self.__key_modified["percent_partial_save"] = 1

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
