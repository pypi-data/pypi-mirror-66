from ..util import Model


class Theme(Model):
	def __init__(self):
		self.__background = None
		self.__new_background = None
		self.__screen = None
		self.__type = None
		self.__normal_tab = None
		self.__selected_tab = None
		self.__key_modified = dict()

	def get_background(self):
		"""
		This method gets the background

		Returns:
		String : A string value
		"""

		return self.__background

	def set_background(self, background):
		"""
		This method sets the value to background

		Parameters:
		background (string) : A string value
		"""

		self.__background = background
		self.__key_modified["background"] = 1

	def get_new_background(self):
		"""
		This method gets the new_background

		Returns:
		String : A string value
		"""

		return self.__new_background

	def set_new_background(self, new_background):
		"""
		This method sets the value to new_background

		Parameters:
		new_background (string) : A string value
		"""

		self.__new_background = new_background
		self.__key_modified["new_background"] = 1

	def get_screen(self):
		"""
		This method gets the screen

		Returns:
		String : A string value
		"""

		return self.__screen

	def set_screen(self, screen):
		"""
		This method sets the value to screen

		Parameters:
		screen (string) : A string value
		"""

		self.__screen = screen
		self.__key_modified["screen"] = 1

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

	def get_normal_tab(self):
		"""
		This method gets the normal_tab

		Returns:
		TabTheme : An instance of TabTheme
		"""

		return self.__normal_tab

	def set_normal_tab(self, normal_tab):
		"""
		This method sets the value to normal_tab

		Parameters:
		normal_tab (TabTheme) : An instance of TabTheme
		"""

		self.__normal_tab = normal_tab
		self.__key_modified["normal_tab"] = 1

	def get_selected_tab(self):
		"""
		This method gets the selected_tab

		Returns:
		TabTheme : An instance of TabTheme
		"""

		return self.__selected_tab

	def set_selected_tab(self, selected_tab):
		"""
		This method sets the value to selected_tab

		Parameters:
		selected_tab (TabTheme) : An instance of TabTheme
		"""

		self.__selected_tab = selected_tab
		self.__key_modified["selected_tab"] = 1

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
