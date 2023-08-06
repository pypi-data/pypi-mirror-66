from ..util import APIResponse
from ..util import CommonAPIHandler

class TaxesOperations(object):
	def __init__(self):
		pass


	def get_taxes(self):
		"""
		This method is used to get taxes

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org/taxes"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_tax(self, request):
		"""
		This method is used to create tax

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org/taxes"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_tax(self, request):
		"""
		This method is used to update tax

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org/taxes"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_tax(self, id):
		"""
		This method is used to get tax

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org/taxes/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def delete_tax(self, id):
		"""
		This method is used to delete tax

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/org/taxes/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
