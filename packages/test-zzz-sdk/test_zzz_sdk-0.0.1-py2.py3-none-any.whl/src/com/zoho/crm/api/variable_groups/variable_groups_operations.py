from ..util import APIResponse
from ..util import CommonAPIHandler

class VariableGroupsOperations(object):
	def __init__(self):
		pass


	def get_variable_groups(self):
		"""
		This method is used to get variable groups

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variable_groups"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_variable_group_by_id(self, id):
		"""
		This method is used to get variable group by id

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variable_groups/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_variable_group_by_api_name(self, api_name):
		"""
		This method is used to get variable group by api name

		Parameters:
		api_name (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variable_groups/"
		api_path = api_path + api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
