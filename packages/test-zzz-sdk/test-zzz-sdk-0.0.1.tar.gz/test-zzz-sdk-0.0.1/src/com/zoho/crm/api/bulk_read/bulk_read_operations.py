from ..util import APIResponse
from ..util import CommonAPIHandler

class BulkReadOperations(object):
	def __init__(self):
		pass


	def get_bulk_read_job_details(self, job_id):
		"""
		This method is used to get bulk read job details

		Parameters:
		job_id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/bulk/v2/read/"
		api_path = api_path + job_id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")

	def download_result(self, job_id):
		"""
		This method is used to download result

		Parameters:
		job_id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/bulk/v2/read/"
		api_path = api_path + job_id.__str__()
		api_path = api_path + "/result"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .file_body_wrapper import FileBodyWrapper
		return handler_instance.api_call(FileBodyWrapper.__module__, "application/json")

	def create_bulk_read_job(self):
		"""
		This method is used to create bulk read job

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/bulk/v2/read"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		from .response_wrapper import ResponseWrapper
		return handler_instance.api_call(ResponseWrapper.__module__, "application/json")
