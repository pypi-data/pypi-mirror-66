from ..util import Model


class User(Model):
	def __init__(self):
		self.__id = None
		self.__country = None
		self.__city = None
		self.__signature = None
		self.__name_format = None
		self.__language = None
		self.__locale = None
		self.__personal_account = None
		self.__default_tab_group = None
		self.__street = None
		self.__alias = None
		self.__state = None
		self.__country_locale = None
		self.__first_name = None
		self.__email = None
		self.__zip = None
		self.__decimal_separator = None
		self.__website = None
		self.__time_format = None
		self.__mobile = None
		self.__last_name = None
		self.__time_zone = None
		self.__zuid = None
		self.__confirm = None
		self.__full_name = None
		self.__phone = None
		self.__dob = None
		self.__date_format = None
		self.__status = None
		self.__profile = None
		self.__role = None
		self.__territories = None
		self.__theme = None
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

	def get_country(self):
		"""
		This method gets the country

		Returns:
		String : A string value
		"""

		return self.__country

	def set_country(self, country):
		"""
		This method sets the value to country

		Parameters:
		country (string) : A string value
		"""

		self.__country = country
		self.__key_modified["country"] = 1

	def get_city(self):
		"""
		This method gets the city

		Returns:
		String : A string value
		"""

		return self.__city

	def set_city(self, city):
		"""
		This method sets the value to city

		Parameters:
		city (string) : A string value
		"""

		self.__city = city
		self.__key_modified["city"] = 1

	def get_signature(self):
		"""
		This method gets the signature

		Returns:
		String : A string value
		"""

		return self.__signature

	def set_signature(self, signature):
		"""
		This method sets the value to signature

		Parameters:
		signature (string) : A string value
		"""

		self.__signature = signature
		self.__key_modified["signature"] = 1

	def get_name_format(self):
		"""
		This method gets the name_format

		Returns:
		String : A string value
		"""

		return self.__name_format

	def set_name_format(self, name_format):
		"""
		This method sets the value to name_format

		Parameters:
		name_format (string) : A string value
		"""

		self.__name_format = name_format
		self.__key_modified["name_format"] = 1

	def get_language(self):
		"""
		This method gets the language

		Returns:
		String : A string value
		"""

		return self.__language

	def set_language(self, language):
		"""
		This method sets the value to language

		Parameters:
		language (string) : A string value
		"""

		self.__language = language
		self.__key_modified["language"] = 1

	def get_locale(self):
		"""
		This method gets the locale

		Returns:
		String : A string value
		"""

		return self.__locale

	def set_locale(self, locale):
		"""
		This method sets the value to locale

		Parameters:
		locale (string) : A string value
		"""

		self.__locale = locale
		self.__key_modified["locale"] = 1

	def get_personal_account(self):
		"""
		This method gets the personal_account

		Returns:
		Boolean : A Boolean value
		"""

		return self.__personal_account

	def set_personal_account(self, personal_account):
		"""
		This method sets the value to personal_account

		Parameters:
		personal_account (Boolean) : A Boolean value
		"""

		self.__personal_account = personal_account
		self.__key_modified["personal_account"] = 1

	def get_default_tab_group(self):
		"""
		This method gets the default_tab_group

		Returns:
		String : A string value
		"""

		return self.__default_tab_group

	def set_default_tab_group(self, default_tab_group):
		"""
		This method sets the value to default_tab_group

		Parameters:
		default_tab_group (string) : A string value
		"""

		self.__default_tab_group = default_tab_group
		self.__key_modified["default_tab_group"] = 1

	def get_street(self):
		"""
		This method gets the street

		Returns:
		String : A string value
		"""

		return self.__street

	def set_street(self, street):
		"""
		This method sets the value to street

		Parameters:
		street (string) : A string value
		"""

		self.__street = street
		self.__key_modified["street"] = 1

	def get_alias(self):
		"""
		This method gets the alias

		Returns:
		String : A string value
		"""

		return self.__alias

	def set_alias(self, alias):
		"""
		This method sets the value to alias

		Parameters:
		alias (string) : A string value
		"""

		self.__alias = alias
		self.__key_modified["alias"] = 1

	def get_state(self):
		"""
		This method gets the state

		Returns:
		String : A string value
		"""

		return self.__state

	def set_state(self, state):
		"""
		This method sets the value to state

		Parameters:
		state (string) : A string value
		"""

		self.__state = state
		self.__key_modified["state"] = 1

	def get_country_locale(self):
		"""
		This method gets the country_locale

		Returns:
		String : A string value
		"""

		return self.__country_locale

	def set_country_locale(self, country_locale):
		"""
		This method sets the value to country_locale

		Parameters:
		country_locale (string) : A string value
		"""

		self.__country_locale = country_locale
		self.__key_modified["country_locale"] = 1

	def get_first_name(self):
		"""
		This method gets the first_name

		Returns:
		String : A string value
		"""

		return self.__first_name

	def set_first_name(self, first_name):
		"""
		This method sets the value to first_name

		Parameters:
		first_name (string) : A string value
		"""

		self.__first_name = first_name
		self.__key_modified["first_name"] = 1

	def get_email(self):
		"""
		This method gets the email

		Returns:
		String : A string value
		"""

		return self.__email

	def set_email(self, email):
		"""
		This method sets the value to email

		Parameters:
		email (string) : A string value
		"""

		self.__email = email
		self.__key_modified["email"] = 1

	def get_zip(self):
		"""
		This method gets the zip

		Returns:
		String : A string value
		"""

		return self.__zip

	def set_zip(self, zip):
		"""
		This method sets the value to zip

		Parameters:
		zip (string) : A string value
		"""

		self.__zip = zip
		self.__key_modified["zip"] = 1

	def get_decimal_separator(self):
		"""
		This method gets the decimal_separator

		Returns:
		String : A string value
		"""

		return self.__decimal_separator

	def set_decimal_separator(self, decimal_separator):
		"""
		This method sets the value to decimal_separator

		Parameters:
		decimal_separator (string) : A string value
		"""

		self.__decimal_separator = decimal_separator
		self.__key_modified["decimal_separator"] = 1

	def get_website(self):
		"""
		This method gets the website

		Returns:
		String : A string value
		"""

		return self.__website

	def set_website(self, website):
		"""
		This method sets the value to website

		Parameters:
		website (string) : A string value
		"""

		self.__website = website
		self.__key_modified["website"] = 1

	def get_time_format(self):
		"""
		This method gets the time_format

		Returns:
		String : A string value
		"""

		return self.__time_format

	def set_time_format(self, time_format):
		"""
		This method sets the value to time_format

		Parameters:
		time_format (string) : A string value
		"""

		self.__time_format = time_format
		self.__key_modified["time_format"] = 1

	def get_mobile(self):
		"""
		This method gets the mobile

		Returns:
		String : A string value
		"""

		return self.__mobile

	def set_mobile(self, mobile):
		"""
		This method sets the value to mobile

		Parameters:
		mobile (string) : A string value
		"""

		self.__mobile = mobile
		self.__key_modified["mobile"] = 1

	def get_last_name(self):
		"""
		This method gets the last_name

		Returns:
		String : A string value
		"""

		return self.__last_name

	def set_last_name(self, last_name):
		"""
		This method sets the value to last_name

		Parameters:
		last_name (string) : A string value
		"""

		self.__last_name = last_name
		self.__key_modified["last_name"] = 1

	def get_time_zone(self):
		"""
		This method gets the time_zone

		Returns:
		String : A string value
		"""

		return self.__time_zone

	def set_time_zone(self, time_zone):
		"""
		This method sets the value to time_zone

		Parameters:
		time_zone (string) : A string value
		"""

		self.__time_zone = time_zone
		self.__key_modified["time_zone"] = 1

	def get_zuid(self):
		"""
		This method gets the zuid

		Returns:
		String : A string value
		"""

		return self.__zuid

	def set_zuid(self, zuid):
		"""
		This method sets the value to zuid

		Parameters:
		zuid (string) : A string value
		"""

		self.__zuid = zuid
		self.__key_modified["zuid"] = 1

	def get_confirm(self):
		"""
		This method gets the confirm

		Returns:
		Boolean : A Boolean value
		"""

		return self.__confirm

	def set_confirm(self, confirm):
		"""
		This method sets the value to confirm

		Parameters:
		confirm (Boolean) : A Boolean value
		"""

		self.__confirm = confirm
		self.__key_modified["confirm"] = 1

	def get_full_name(self):
		"""
		This method gets the full_name

		Returns:
		String : A string value
		"""

		return self.__full_name

	def set_full_name(self, full_name):
		"""
		This method sets the value to full_name

		Parameters:
		full_name (string) : A string value
		"""

		self.__full_name = full_name
		self.__key_modified["full_name"] = 1

	def get_phone(self):
		"""
		This method gets the phone

		Returns:
		String : A string value
		"""

		return self.__phone

	def set_phone(self, phone):
		"""
		This method sets the value to phone

		Parameters:
		phone (string) : A string value
		"""

		self.__phone = phone
		self.__key_modified["phone"] = 1

	def get_dob(self):
		"""
		This method gets the dob

		Returns:
		String : A string value
		"""

		return self.__dob

	def set_dob(self, dob):
		"""
		This method sets the value to dob

		Parameters:
		dob (string) : A string value
		"""

		self.__dob = dob
		self.__key_modified["dob"] = 1

	def get_date_format(self):
		"""
		This method gets the date_format

		Returns:
		String : A string value
		"""

		return self.__date_format

	def set_date_format(self, date_format):
		"""
		This method sets the value to date_format

		Parameters:
		date_format (string) : A string value
		"""

		self.__date_format = date_format
		self.__key_modified["date_format"] = 1

	def get_status(self):
		"""
		This method gets the status

		Returns:
		String : A string value
		"""

		return self.__status

	def set_status(self, status):
		"""
		This method sets the value to status

		Parameters:
		status (string) : A string value
		"""

		self.__status = status
		self.__key_modified["status"] = 1

	def get_profile(self):
		"""
		This method gets the profile

		Returns:
		Profile : An instance of Profile
		"""

		return self.__profile

	def set_profile(self, profile):
		"""
		This method sets the value to profile

		Parameters:
		profile (Profile) : An instance of Profile
		"""

		self.__profile = profile
		self.__key_modified["profile"] = 1

	def get_role(self):
		"""
		This method gets the role

		Returns:
		Profile : An instance of Profile
		"""

		return self.__role

	def set_role(self, role):
		"""
		This method sets the value to role

		Parameters:
		role (Profile) : An instance of Profile
		"""

		self.__role = role
		self.__key_modified["role"] = 1

	def get_territories(self):
		"""
		This method gets the territories

		Returns:
		List : An instance of List
		"""

		return self.__territories

	def set_territories(self, territories):
		"""
		This method sets the value to territories

		Parameters:
		territories (List) : An instance of List
		"""

		self.__territories = territories
		self.__key_modified["territories"] = 1

	def get_theme(self):
		"""
		This method gets the theme

		Returns:
		Theme : An instance of Theme
		"""

		return self.__theme

	def set_theme(self, theme):
		"""
		This method sets the value to theme

		Parameters:
		theme (Theme) : An instance of Theme
		"""

		self.__theme = theme
		self.__key_modified["theme"] = 1

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
