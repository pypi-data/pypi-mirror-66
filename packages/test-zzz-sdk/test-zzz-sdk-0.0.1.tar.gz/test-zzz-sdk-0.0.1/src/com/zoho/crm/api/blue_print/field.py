from ..util import Model


class Field(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__display_label = None
		self.__data_type = None
		self.__column_name = None
		self.__transition_sequence = None
		self.__mandatory = None
		self.__content = None
		self.__system_mandatory = None
		self.__webhook = None
		self.__json_type = None
		self.__crypt = None
		self.__field_label = None
		self.__tooltip = None
		self.__created_source = None
		self.__field_read_only = None
		self.__validation_rule = None
		self.__read_only = None
		self.__association_details = None
		self.__quick_sequence_number = None
		self.__custom_field = None
		self.__visible = None
		self.__length = None
		self.__decimal_place = None
		self.__view_type = None
		self.__pick_list_values = None
		self.__multiselectlookup = None
		self.__auto_number = None
		self.__layouts = None
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
		Long : A string value
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

	def get_data_type(self):
		"""
		This method gets the data_type

		Returns:
		String : A string value
		"""

		return self.__data_type

	def set_data_type(self, data_type):
		"""
		This method sets the value to data_type

		Parameters:
		data_type (string) : A string value
		"""

		self.__data_type = data_type
		self.__key_modified["data_type"] = 1

	def get_column_name(self):
		"""
		This method gets the column_name

		Returns:
		String : A string value
		"""

		return self.__column_name

	def set_column_name(self, column_name):
		"""
		This method sets the value to column_name

		Parameters:
		column_name (string) : A string value
		"""

		self.__column_name = column_name
		self.__key_modified["column_name"] = 1

	def get_transition_sequence(self):
		"""
		This method gets the transition_sequence

		Returns:
		Integer : A int value
		"""

		return self.__transition_sequence

	def set_transition_sequence(self, transition_sequence):
		"""
		This method sets the value to transition_sequence

		Parameters:
		transition_sequence (int) : A int value
		"""

		self.__transition_sequence = transition_sequence
		self.__key_modified["transition_sequence"] = 1

	def get_mandatory(self):
		"""
		This method gets the mandatory

		Returns:
		Boolean : A Boolean value
		"""

		return self.__mandatory

	def set_mandatory(self, mandatory):
		"""
		This method sets the value to mandatory

		Parameters:
		mandatory (Boolean) : A Boolean value
		"""

		self.__mandatory = mandatory
		self.__key_modified["mandatory"] = 1

	def get_content(self):
		"""
		This method gets the content

		Returns:
		String : A string value
		"""

		return self.__content

	def set_content(self, content):
		"""
		This method sets the value to content

		Parameters:
		content (string) : A string value
		"""

		self.__content = content
		self.__key_modified["content"] = 1

	def get_system_mandatory(self):
		"""
		This method gets the system_mandatory

		Returns:
		Boolean : A Boolean value
		"""

		return self.__system_mandatory

	def set_system_mandatory(self, system_mandatory):
		"""
		This method sets the value to system_mandatory

		Parameters:
		system_mandatory (Boolean) : A Boolean value
		"""

		self.__system_mandatory = system_mandatory
		self.__key_modified["system_mandatory"] = 1

	def get_webhook(self):
		"""
		This method gets the webhook

		Returns:
		Boolean : A Boolean value
		"""

		return self.__webhook

	def set_webhook(self, webhook):
		"""
		This method sets the value to webhook

		Parameters:
		webhook (Boolean) : A Boolean value
		"""

		self.__webhook = webhook
		self.__key_modified["webhook"] = 1

	def get_json_type(self):
		"""
		This method gets the json_type

		Returns:
		String : A string value
		"""

		return self.__json_type

	def set_json_type(self, json_type):
		"""
		This method sets the value to json_type

		Parameters:
		json_type (string) : A string value
		"""

		self.__json_type = json_type
		self.__key_modified["json_type"] = 1

	def get_crypt(self):
		"""
		This method gets the crypt

		Returns:
		String : A string value
		"""

		return self.__crypt

	def set_crypt(self, crypt):
		"""
		This method sets the value to crypt

		Parameters:
		crypt (string) : A string value
		"""

		self.__crypt = crypt
		self.__key_modified["crypt"] = 1

	def get_field_label(self):
		"""
		This method gets the field_label

		Returns:
		String : A string value
		"""

		return self.__field_label

	def set_field_label(self, field_label):
		"""
		This method sets the value to field_label

		Parameters:
		field_label (string) : A string value
		"""

		self.__field_label = field_label
		self.__key_modified["field_label"] = 1

	def get_tooltip(self):
		"""
		This method gets the tooltip

		Returns:
		String : A string value
		"""

		return self.__tooltip

	def set_tooltip(self, tooltip):
		"""
		This method sets the value to tooltip

		Parameters:
		tooltip (string) : A string value
		"""

		self.__tooltip = tooltip
		self.__key_modified["tooltip"] = 1

	def get_created_source(self):
		"""
		This method gets the created_source

		Returns:
		String : A string value
		"""

		return self.__created_source

	def set_created_source(self, created_source):
		"""
		This method sets the value to created_source

		Parameters:
		created_source (string) : A string value
		"""

		self.__created_source = created_source
		self.__key_modified["created_source"] = 1

	def get_field_read_only(self):
		"""
		This method gets the field_read_only

		Returns:
		Boolean : A Boolean value
		"""

		return self.__field_read_only

	def set_field_read_only(self, field_read_only):
		"""
		This method sets the value to field_read_only

		Parameters:
		field_read_only (Boolean) : A Boolean value
		"""

		self.__field_read_only = field_read_only
		self.__key_modified["field_read_only"] = 1

	def get_validation_rule(self):
		"""
		This method gets the validation_rule

		Returns:
		String : A string value
		"""

		return self.__validation_rule

	def set_validation_rule(self, validation_rule):
		"""
		This method sets the value to validation_rule

		Parameters:
		validation_rule (string) : A string value
		"""

		self.__validation_rule = validation_rule
		self.__key_modified["validation_rule"] = 1

	def get_read_only(self):
		"""
		This method gets the read_only

		Returns:
		Boolean : A Boolean value
		"""

		return self.__read_only

	def set_read_only(self, read_only):
		"""
		This method sets the value to read_only

		Parameters:
		read_only (Boolean) : A Boolean value
		"""

		self.__read_only = read_only
		self.__key_modified["read_only"] = 1

	def get_association_details(self):
		"""
		This method gets the association_details

		Returns:
		String : A string value
		"""

		return self.__association_details

	def set_association_details(self, association_details):
		"""
		This method sets the value to association_details

		Parameters:
		association_details (string) : A string value
		"""

		self.__association_details = association_details
		self.__key_modified["association_details"] = 1

	def get_quick_sequence_number(self):
		"""
		This method gets the quick_sequence_number

		Returns:
		Long : A string value
		"""

		return self.__quick_sequence_number

	def set_quick_sequence_number(self, quick_sequence_number):
		"""
		This method sets the value to quick_sequence_number

		Parameters:
		quick_sequence_number (string) : A string value
		"""

		self.__quick_sequence_number = quick_sequence_number
		self.__key_modified["quick_sequence_number"] = 1

	def get_custom_field(self):
		"""
		This method gets the custom_field

		Returns:
		Boolean : A Boolean value
		"""

		return self.__custom_field

	def set_custom_field(self, custom_field):
		"""
		This method sets the value to custom_field

		Parameters:
		custom_field (Boolean) : A Boolean value
		"""

		self.__custom_field = custom_field
		self.__key_modified["custom_field"] = 1

	def get_visible(self):
		"""
		This method gets the visible

		Returns:
		Boolean : A Boolean value
		"""

		return self.__visible

	def set_visible(self, visible):
		"""
		This method sets the value to visible

		Parameters:
		visible (Boolean) : A Boolean value
		"""

		self.__visible = visible
		self.__key_modified["visible"] = 1

	def get_length(self):
		"""
		This method gets the length

		Returns:
		Integer : A int value
		"""

		return self.__length

	def set_length(self, length):
		"""
		This method sets the value to length

		Parameters:
		length (int) : A int value
		"""

		self.__length = length
		self.__key_modified["length"] = 1

	def get_decimal_place(self):
		"""
		This method gets the decimal_place

		Returns:
		String : A string value
		"""

		return self.__decimal_place

	def set_decimal_place(self, decimal_place):
		"""
		This method sets the value to decimal_place

		Parameters:
		decimal_place (string) : A string value
		"""

		self.__decimal_place = decimal_place
		self.__key_modified["decimal_place"] = 1

	def get_view_type(self):
		"""
		This method gets the view_type

		Returns:
		ViewType : An instance of ViewType
		"""

		return self.__view_type

	def set_view_type(self, view_type):
		"""
		This method sets the value to view_type

		Parameters:
		view_type (ViewType) : An instance of ViewType
		"""

		self.__view_type = view_type
		self.__key_modified["view_type"] = 1

	def get_pick_list_values(self):
		"""
		This method gets the pick_list_values

		Returns:
		List : An instance of List
		"""

		return self.__pick_list_values

	def set_pick_list_values(self, pick_list_values):
		"""
		This method sets the value to pick_list_values

		Parameters:
		pick_list_values (List) : An instance of List
		"""

		self.__pick_list_values = pick_list_values
		self.__key_modified["pick_list_values"] = 1

	def get_multiselectlookup(self):
		"""
		This method gets the multiselectlookup

		Returns:
		Map : An instance of Map
		"""

		return self.__multiselectlookup

	def set_multiselectlookup(self, multiselectlookup):
		"""
		This method sets the value to multiselectlookup

		Parameters:
		multiselectlookup (Map) : An instance of Map
		"""

		self.__multiselectlookup = multiselectlookup
		self.__key_modified["multiselectlookup"] = 1

	def get_auto_number(self):
		"""
		This method gets the auto_number

		Returns:
		Map : An instance of Map
		"""

		return self.__auto_number

	def set_auto_number(self, auto_number):
		"""
		This method sets the value to auto_number

		Parameters:
		auto_number (Map) : An instance of Map
		"""

		self.__auto_number = auto_number
		self.__key_modified["auto_number"] = 1

	def get_layouts(self):
		"""
		This method gets the layouts

		Returns:
		List : An instance of List
		"""

		return self.__layouts

	def set_layouts(self, layouts):
		"""
		This method sets the value to layouts

		Parameters:
		layouts (List) : An instance of List
		"""

		self.__layouts = layouts
		self.__key_modified["layouts"] = 1

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
