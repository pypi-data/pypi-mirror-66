from ..util import APIResponse
from ..util import CommonAPIHandler

class AttachmentsOperations(object):
	def __init__(self,record_id,module_api_name):
		self.__record_id = record_id
		self.__module_api_name = module_api_name



	def download_attachment(self, id):
		"""
		This method is used to download attachment

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__record_id.__str__()
		api_path = api_path + "/Attachments/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .file_body_wrapper import FileBodyWrapper
		return handler_instance.api_call(FileBodyWrapper.__module__, "application/x-download")

	def delete_attachment(self, id):
		"""
		This method is used to delete attachment

		Parameters:
		id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__record_id.__str__()
		api_path = api_path + "/Attachments/"
		api_path = api_path + id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "DELETE"
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def get_attachments(self):
		"""
		This method is used to get attachments

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__record_id.__str__()
		api_path = api_path + "/Attachments"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def upload_attachment(self, request):
		"""
		This method is used to upload attachment

		Parameters:
		request (FileBodyWrapper) : An instance of FileBodyWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__record_id.__str__()
		api_path = api_path + "/Attachments"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "multipart/form-data"
		handler_instance.request = request
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")
