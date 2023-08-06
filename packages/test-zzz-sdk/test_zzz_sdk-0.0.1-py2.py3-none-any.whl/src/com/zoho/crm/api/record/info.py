from ..util import Model


class Info(Model):
	def __init__(self):
		self.__per_page = None
		self.__count = None
		self.__page = None
		self.__more_records = None
		self.__key_modified = dict()

	def get_per_page(self):
		"""
		This method gets the per_page

		Returns:
		Integer : A int value
		"""

		return self.__per_page

	def set_per_page(self, per_page):
		"""
		This method sets the value to per_page

		Parameters:
		per_page (int) : A int value
		"""

		self.__per_page = per_page
		self.__key_modified["per_page"] = 1

	def get_count(self):
		"""
		This method gets the count

		Returns:
		Integer : A int value
		"""

		return self.__count

	def set_count(self, count):
		"""
		This method sets the value to count

		Parameters:
		count (int) : A int value
		"""

		self.__count = count
		self.__key_modified["count"] = 1

	def get_page(self):
		"""
		This method gets the page

		Returns:
		Integer : A int value
		"""

		return self.__page

	def set_page(self, page):
		"""
		This method sets the value to page

		Parameters:
		page (int) : A int value
		"""

		self.__page = page
		self.__key_modified["page"] = 1

	def get_more_records(self):
		"""
		This method gets the more_records

		Returns:
		Boolean : A Boolean value
		"""

		return self.__more_records

	def set_more_records(self, more_records):
		"""
		This method sets the value to more_records

		Parameters:
		more_records (Boolean) : A Boolean value
		"""

		self.__more_records = more_records
		self.__key_modified["more_records"] = 1

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
