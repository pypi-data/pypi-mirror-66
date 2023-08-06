from ..util import APIResponse
from ..util import CommonAPIHandler

class RelatedListOperations(object):
	def __init__(self,module_api_name):
		self.__module_api_name = module_api_name


	def get_related_list(self):
		"""
		This method is used to get related list

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/related_lists"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.add_param("module_api_name", self.__module_api_name)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_related_list(self, id):
		"""
		This method is used to get related list

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/related_lists/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.add_param("module_api_name", self.__module_api_name)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
