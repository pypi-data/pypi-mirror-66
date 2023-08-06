from ..util import Model


class Org(Model):
	def __init__(self):
		self.__id = None
		self.__country = None
		self.__photo_id = None
		self.__city = None
		self.__description = None
		self.__mc_status = None
		self.__gapps_enabled = None
		self.__translation_enabled = None
		self.__street = None
		self.__alias = None
		self.__currency = None
		self.__state = None
		self.__fax = None
		self.__employee_count = None
		self.__zip = None
		self.__website = None
		self.__currency_symbol = None
		self.__mobile = None
		self.__currency_locale = None
		self.__primary_zuid = None
		self.__zia_portal_id = None
		self.__time_zone = None
		self.__zgid = None
		self.__country_code = None
		self.__phone = None
		self.__company_name = None
		self.__privacy_settings = None
		self.__primary_email = None
		self.__iso_code = None
		self.__license_details = None
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

	def get_photo_id(self):
		"""
		This method gets the photo_id

		Returns:
		String : A string value
		"""

		return self.__photo_id

	def set_photo_id(self, photo_id):
		"""
		This method sets the value to photo_id

		Parameters:
		photo_id (string) : A string value
		"""

		self.__photo_id = photo_id
		self.__key_modified["photo_id"] = 1

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

	def get_description(self):
		"""
		This method gets the description

		Returns:
		String : A string value
		"""

		return self.__description

	def set_description(self, description):
		"""
		This method sets the value to description

		Parameters:
		description (string) : A string value
		"""

		self.__description = description
		self.__key_modified["description"] = 1

	def get_mc_status(self):
		"""
		This method gets the mc_status

		Returns:
		Boolean : A Boolean value
		"""

		return self.__mc_status

	def set_mc_status(self, mc_status):
		"""
		This method sets the value to mc_status

		Parameters:
		mc_status (Boolean) : A Boolean value
		"""

		self.__mc_status = mc_status
		self.__key_modified["mc_status"] = 1

	def get_gapps_enabled(self):
		"""
		This method gets the gapps_enabled

		Returns:
		Boolean : A Boolean value
		"""

		return self.__gapps_enabled

	def set_gapps_enabled(self, gapps_enabled):
		"""
		This method sets the value to gapps_enabled

		Parameters:
		gapps_enabled (Boolean) : A Boolean value
		"""

		self.__gapps_enabled = gapps_enabled
		self.__key_modified["gapps_enabled"] = 1

	def get_translation_enabled(self):
		"""
		This method gets the translation_enabled

		Returns:
		Boolean : A Boolean value
		"""

		return self.__translation_enabled

	def set_translation_enabled(self, translation_enabled):
		"""
		This method sets the value to translation_enabled

		Parameters:
		translation_enabled (Boolean) : A Boolean value
		"""

		self.__translation_enabled = translation_enabled
		self.__key_modified["translation_enabled"] = 1

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

	def get_currency(self):
		"""
		This method gets the currency

		Returns:
		String : A string value
		"""

		return self.__currency

	def set_currency(self, currency):
		"""
		This method sets the value to currency

		Parameters:
		currency (string) : A string value
		"""

		self.__currency = currency
		self.__key_modified["currency"] = 1

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

	def get_fax(self):
		"""
		This method gets the fax

		Returns:
		String : A string value
		"""

		return self.__fax

	def set_fax(self, fax):
		"""
		This method sets the value to fax

		Parameters:
		fax (string) : A string value
		"""

		self.__fax = fax
		self.__key_modified["fax"] = 1

	def get_employee_count(self):
		"""
		This method gets the employee_count

		Returns:
		String : A string value
		"""

		return self.__employee_count

	def set_employee_count(self, employee_count):
		"""
		This method sets the value to employee_count

		Parameters:
		employee_count (string) : A string value
		"""

		self.__employee_count = employee_count
		self.__key_modified["employee_count"] = 1

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

	def get_currency_symbol(self):
		"""
		This method gets the currency_symbol

		Returns:
		String : A string value
		"""

		return self.__currency_symbol

	def set_currency_symbol(self, currency_symbol):
		"""
		This method sets the value to currency_symbol

		Parameters:
		currency_symbol (string) : A string value
		"""

		self.__currency_symbol = currency_symbol
		self.__key_modified["currency_symbol"] = 1

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

	def get_currency_locale(self):
		"""
		This method gets the currency_locale

		Returns:
		String : A string value
		"""

		return self.__currency_locale

	def set_currency_locale(self, currency_locale):
		"""
		This method sets the value to currency_locale

		Parameters:
		currency_locale (string) : A string value
		"""

		self.__currency_locale = currency_locale
		self.__key_modified["currency_locale"] = 1

	def get_primary_zuid(self):
		"""
		This method gets the primary_zuid

		Returns:
		String : A string value
		"""

		return self.__primary_zuid

	def set_primary_zuid(self, primary_zuid):
		"""
		This method sets the value to primary_zuid

		Parameters:
		primary_zuid (string) : A string value
		"""

		self.__primary_zuid = primary_zuid
		self.__key_modified["primary_zuid"] = 1

	def get_zia_portal_id(self):
		"""
		This method gets the zia_portal_id

		Returns:
		String : A string value
		"""

		return self.__zia_portal_id

	def set_zia_portal_id(self, zia_portal_id):
		"""
		This method sets the value to zia_portal_id

		Parameters:
		zia_portal_id (string) : A string value
		"""

		self.__zia_portal_id = zia_portal_id
		self.__key_modified["zia_portal_id"] = 1

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

	def get_zgid(self):
		"""
		This method gets the zgid

		Returns:
		String : A string value
		"""

		return self.__zgid

	def set_zgid(self, zgid):
		"""
		This method sets the value to zgid

		Parameters:
		zgid (string) : A string value
		"""

		self.__zgid = zgid
		self.__key_modified["zgid"] = 1

	def get_country_code(self):
		"""
		This method gets the country_code

		Returns:
		String : A string value
		"""

		return self.__country_code

	def set_country_code(self, country_code):
		"""
		This method sets the value to country_code

		Parameters:
		country_code (string) : A string value
		"""

		self.__country_code = country_code
		self.__key_modified["country_code"] = 1

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

	def get_company_name(self):
		"""
		This method gets the company_name

		Returns:
		String : A string value
		"""

		return self.__company_name

	def set_company_name(self, company_name):
		"""
		This method sets the value to company_name

		Parameters:
		company_name (string) : A string value
		"""

		self.__company_name = company_name
		self.__key_modified["company_name"] = 1

	def get_privacy_settings(self):
		"""
		This method gets the privacy_settings

		Returns:
		Boolean : A Boolean value
		"""

		return self.__privacy_settings

	def set_privacy_settings(self, privacy_settings):
		"""
		This method sets the value to privacy_settings

		Parameters:
		privacy_settings (Boolean) : A Boolean value
		"""

		self.__privacy_settings = privacy_settings
		self.__key_modified["privacy_settings"] = 1

	def get_primary_email(self):
		"""
		This method gets the primary_email

		Returns:
		String : A string value
		"""

		return self.__primary_email

	def set_primary_email(self, primary_email):
		"""
		This method sets the value to primary_email

		Parameters:
		primary_email (string) : A string value
		"""

		self.__primary_email = primary_email
		self.__key_modified["primary_email"] = 1

	def get_iso_code(self):
		"""
		This method gets the iso_code

		Returns:
		String : A string value
		"""

		return self.__iso_code

	def set_iso_code(self, iso_code):
		"""
		This method sets the value to iso_code

		Parameters:
		iso_code (string) : A string value
		"""

		self.__iso_code = iso_code
		self.__key_modified["iso_code"] = 1

	def get_license_details(self):
		"""
		This method gets the license_details

		Returns:
		Map : An instance of Map
		"""

		return self.__license_details

	def set_license_details(self, license_details):
		"""
		This method sets the value to license_details

		Parameters:
		license_details (Map) : An instance of Map
		"""

		self.__license_details = license_details
		self.__key_modified["license_details"] = 1

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
