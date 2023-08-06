from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class VariablesOperations(object):
	def __init__(self):
		pass


	def get_variables(self, param_instance, id):
		"""
		This method is used to get variables

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_variables(self, request):
		"""
		This method is used to create variables

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def update_variables(self, request):
		"""
		This method is used to update variables

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables"
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_variables(self, request):
		"""
		This method is used to delete variables

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables"
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_variable_by_id(self, param_instance, id):
		"""
		This method is used to get variable by id

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_variable_by_group_api_name(self, param_instance, id):
		"""
		This method is used to get variable by group api name

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_variable_by_id(self, request, id):
		"""
		This method is used to update variable by id

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_variable(self, id):
		"""
		This method is used to delete variable

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_variable_for_group_id(self, param_instance, api_name):
		"""
		This method is used to get variable for group id

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap
		api_name (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_variable_for_group_api_name(self, id, api_name):
		"""
		This method is used to get variable for group api name

		Parameters:
		id (string) : A string value
		api_name (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_variable_by_api_name(self, request, api_name):
		"""
		This method is used to update variable by api name

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		api_name (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_variable_by_api_name(self, api_name):
		"""
		This method is used to delete variable by api name

		Parameters:
		api_name (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/variables/"
		api_path = api_path + api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
class GetVariablesParam(object):
	group_id = Param("group_id")



class GetVariableByIDParam(object):
	group_id = Param("group_id")



class GetVariableByGroupAPINameParam(object):
	group_api_name = Param("group_api_name")



class GetVariableForGroupIDParam(object):
	group_id = Param("group_id")


