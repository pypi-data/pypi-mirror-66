from ..header import Header
from ..header_map import HeaderMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class BulkWriteOperations(object):
	def __init__(self):
		pass


	def upload_file(self, request, header_instance):
		"""
		This method is used to upload file

		Parameters:
		request (FileBodyWrapper) : An instance of FileBodyWrapper
		header_instance (HeaderMap) : An instance of HeaderMap

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/upload"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "multipart/form-data"
		handler_instance.request = request
		handler_instance.header = header_instance
		from .object import Object
		return handler_instance.api_call(Object.__module__, "application/json")

	def create_bulk_write_job(self, request):
		"""
		This method is used to create bulk write job

		Parameters:
		request (RequestWrapper) : An instance of RequestWrapper

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/bulk/v2/write"
		handler_instance.api_path = api_path
		handler_instance.http_method = "POST"
		handler_instance.content_type = "application/json"
		handler_instance.request = request
		from .object import Object
		return handler_instance.api_call(Object.__module__, "application/json")

	def get_bulk_write_job_details(self, job_id):
		"""
		This method is used to get bulk write job details

		Parameters:
		job_id (string) : A string value

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/bulk/v2/write/"
		api_path = api_path + job_id.__str__()
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .bulk_write_response import BulkWriteResponse
		return handler_instance.api_call(BulkWriteResponse.__module__, "application/json")
class UploadFileHeader(object):
	feature = Header("feature")

X_crm_org = Header("X-CRM-ORG")


