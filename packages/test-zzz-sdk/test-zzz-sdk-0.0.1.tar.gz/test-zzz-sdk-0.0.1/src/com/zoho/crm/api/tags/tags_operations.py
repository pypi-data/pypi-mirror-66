from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class TagsOperations(object):
	def __init__(self,tag_names,module_api_name):
		self.__tag_names = tag_names
		self.__module_api_name = module_api_name



	def get_tags(self, param_instance):
		"""
		This method is used to get tags

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_tags(self, request, param_instance):
		"""
		This method is used to create tags

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_tags(self, request, param_instance):
		"""
		This method is used to update tags

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def get_tag(self, param_instance, id):
		"""
		This method is used to get tag

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_tag(self, request, param_instance, id):
		"""
		This method is used to create tag

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_tag(self, request, param_instance, id):
		"""
		This method is used to update tag

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper
		param_instance (ParameterMap) : An instance of ParameterMap
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def delete_tag(self, id):
		"""
		This method is used to delete tag

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def merge_tags(self, request, id):
		"""
		This method is used to merge tags

		Parameters:
		request (MergeWrapper) : An instance of MergeWrapper
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/actions/merge"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		handler_instance.add_param("tag_names", self.__tag_names)
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def add_tags(self, record_id):
		"""
		This method is used to add tags

		Parameters:
		record_id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + record_id.__str__()
		api_path = api_path + "/actions/add_tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.add_param("tag_names", self.__tag_names)
		from .success_response import SuccessResponse
		return handler_instance.api_call(SuccessResponse.__module__, "application/json")

	def delete_tags(self, record_id):
		"""
		This method is used to delete tags

		Parameters:
		record_id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + record_id.__str__()
		api_path = api_path + "/actions/remove_tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.add_param("tag_names", self.__tag_names)
		from .success_response import SuccessResponse
		return handler_instance.api_call(SuccessResponse.__module__, "application/json")

	def add_tags(self, param_instance):
		"""
		This method is used to add tags

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/actions/add_tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .success_response import SuccessResponse
		return handler_instance.api_call(SuccessResponse.__module__, "application/json")

	def delete_tags(self, param_instance):
		"""
		This method is used to delete tags

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/actions/remove_tags"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.param = param_instance
		handler_instance.add_param("tag_names", self.__tag_names)
		from .success_response import SuccessResponse
		return handler_instance.api_call(SuccessResponse.__module__, "application/json")
class GetTagsParam(object):
	module = Param("module")



class CreateTagsParam(object):
	module = Param("module")



class UpdateTagsParam(object):
	module = Param("module")



class GetTagParam(object):
	module = Param("module")



class CreateTagParam(object):
	module = Param("module")



class UpdateTagParam(object):
	module = Param("module")



class AddTagsParam(object):
	ids = Param("ids")



class DeleteTagsParam(object):
	ids = Param("ids")


