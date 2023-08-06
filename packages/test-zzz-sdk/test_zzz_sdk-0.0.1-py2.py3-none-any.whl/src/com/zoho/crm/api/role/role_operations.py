from ..util import APIResponse
from ..util import CommonAPIHandler

class RoleOperations(object):
	def __init__(self):
		pass


	def get_roles(self):
		"""
		This method is used to get roles

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/roles"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_role(self, id):
		"""
		This method is used to get role

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
