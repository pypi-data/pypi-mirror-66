from ..util import APIResponse
from ..util import CommonAPIHandler

class BluePrintOperations(object):
	def __init__(self,module_api_name,record_id):
		self.__module_api_name = module_api_name
		self.__record_id = record_id



	def get_blueprint(self):
		"""
		This method is used to get blueprint

		Returns:
		APIResponse : An instance of APIResponse
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + self.__module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + self.__record_id.__str__()
		api_path = api_path + "/actions/blueprint"
		handler_instance.api_path = api_path
		handler_instance.http_method = "GET"
		from .object import Object
		return handler_instance.api_call(Object.__module__, "application/x-download")
