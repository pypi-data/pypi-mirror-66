from ..util import Model


class TabTheme(Model):
	def __init__(self):
		self.__font_color = None
		self.__background = None
		self.__key_modified = dict()

	def get_font_color(self):
		"""
		This method gets the font_color

		Returns:
		String : A string value
		"""

		return self.__font_color

	def set_font_color(self, font_color):
		"""
		This method sets the value to font_color

		Parameters:
		font_color (string) : A string value
		"""

		self.__font_color = font_color
		self.__key_modified["font_color"] = 1

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
