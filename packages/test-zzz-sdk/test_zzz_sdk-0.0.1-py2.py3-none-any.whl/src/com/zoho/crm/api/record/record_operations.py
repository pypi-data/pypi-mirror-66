from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler
from ..util import Utility

class RecordOperations(object):
	def __init__(self,module_api_name,id):
		self.__module_api_name = module_api_name
		self.__id = id



	def get_record(self):
		"""
		This method is used to get record

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def update_record(self, request):
		"""
		This method is used to update record

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_record(self, wf_trigger):
		"""
		This method is used to delete record

		Parameters:
		wf_trigger (Boolean) : A Boolean value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_records(self):
		"""
		This method is used to get records

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def create_records(self, request):
		"""
		This method is used to create records

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def update_records(self, request):
		"""
		This method is used to update records

		Parameters:
		request (BodyWrapper) : An instance of BodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_records(self, ids, wf_trigger):
		"""
		This method is used to delete records

		Parameters:
		ids (string) : A string value
		wf_trigger (Boolean) : A Boolean value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def update_records(self, request):
		"""
		This method is used to update records

		Parameters:
		request (UpsertBodyWrapper) : An instance of UpsertBodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/upsert"
		handler_instance.api_path = api_path
		handler_instance.http_method = "PUT"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .upsert_action_wrapper import UpsertActionWrapper
		return handler_instance.api_call(UpsertActionWrapper.__module__, "application/json")

	def get_deleted_records(self):
		"""
		This method is used to get deleted records

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/deleted"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def search_records(self, param_instance):
		"""
		This method is used to search records

		Parameters:
		param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/search"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.param = param_instance
		Utility.get_fields(self.__module_api_name)
		handler_instance.module_api_name = self.__module_api_name
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def convert_lead(self, request):
		"""
		This method is used to convert lead

		Parameters:
		request (ConvertBodyWrapper) : An instance of ConvertBodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Leads/"
		api_path = api_path + self.__id.__str__()
		api_path = api_path + "/actions/convert"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .convert_response_wrapper import ConvertResponseWrapper
		return handler_instance.api_call(ConvertResponseWrapper.__module__, "application/json")

	def get_photo(self):
		"""
		This method is used to get photo

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "https://www.zohoapis.com/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .file_body_wrapper import FileBodyWrapper
		return handler_instance.api_call(FileBodyWrapper.__module__, "application/x-download")

	def create_photo(self, request):
		"""
		This method is used to create photo

		Parameters:
		request (FileBodyWrapper) : An instance of FileBodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "https://www.zohoapis.com/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "multipart/form-data"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def delete_photo(self):
		"""
		This method is used to delete photo

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "https://www.zohoapis.com/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
class SearchRecordsParam(object):
	criteria = Param("criteria")

email = Param("email")

phone = Param("phone")

word = Param("word")

converted = Param("converted")

approved = Param("approved")

page = Param("page")

per_page = Param("per_page")


