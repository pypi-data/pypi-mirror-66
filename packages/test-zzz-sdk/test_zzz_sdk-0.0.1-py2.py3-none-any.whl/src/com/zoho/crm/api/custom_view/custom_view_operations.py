from ..util import APIResponse
from ..util import CommonAPIHandler

class CustomViewOperations(object):
	def __init__(self,module):
		self.__module = module


	def get_custom_views(self):
		"""
		This method is used to get custom views

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/custom_views"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.add_param("module", self.__module)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_custom_view(self, id):
		"""
		This method is used to get custom view

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/custom_views/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.add_param("module", self.__module)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_custom_view(self, request, id):
		"""
		This method is used to update custom view

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/custom_views/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.add_param("module", self.__module)
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
