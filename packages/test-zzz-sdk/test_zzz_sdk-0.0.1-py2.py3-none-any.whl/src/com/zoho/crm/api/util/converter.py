try:

    import logging

    import sys

    import traceback

    import zlib

    import base64

    import re

except Exception:

    import logging

    import sys

    import traceback

    import zlib

    import base64

    import re

if sys.version > '3':

    from abc import ABC, abstractmethod

    class Converter(ABC):

        """
        This abstract class to use construct API request and response.
        """

        logger = logging.getLogger('client_lib')

        def __init__(self, common_api_handler):

            """
            Creates a Converter class instance with the CommonAPIHandler class instance.
            :param common_api_handler: A CommonAPIHandler class instance.
            """

            self.common_api_handler = common_api_handler

        @abstractmethod
        def get_response(self, response, pack):

            """
            This abstract method to process the API response.
            :param response: A object containing the API response contents or response.
            :param pack: A str containing the expected method return type.
            :return: A object representing the POJO class instance.
            """

            pass

        @abstractmethod
        def form_request(self, request_object, pack, instance_number):

            """
            This abstract method to construct the API request.
            :param request_object: A Object containing the POJO class instance.
            :param pack: A str containing the expected method return type.
            :param instance_number: An int containing the POJO class instance list number.
            :return: A object representing the API request body object.
            """

            pass

        @abstractmethod
        def append_to_request(self, request_base, request_object):

            """
            This abstract method to construct the API request body.
            :param request_base: A HttpEntityEnclosingRequestBase class instance.
            :param request_object: A object containing the API request body object.
            """

            pass

        @abstractmethod
        def get_wrapped_response(self, response, pack):

            """
            This abstract method to process the API response.
            :param response: A object containing the HttpResponse class instance.
            :param pack: A str containing the expected method return type.
            :return: A object representing the POJO class instance.
            """
            pass

        def value_checker(self, class_name, member_name, key_details, value, unique_values_map, instance_number):

            """
            This method is to validate if the input values satisfy the constraints for the respective fields.
            :param class_name: A str containing the class name.
            :param member_name: A str containing the member name.
            :param key_details: A JSON object containing the key JSON details.
            :param value: A object containing the key value.
            :param unique_values_map: A list containing the construct objects.
            :param instance_number: An int containing the POJO class instance list number.
            :return: A bool representing the key value is expected pattern, unique, length, and values.
            """

            from src.com.zoho.api.exception import SDKException

            from .constants import Constants

            detailsJO = {}

            name = key_details[Constants.NAME]

            # Data Type Validation
            if key_details[Constants.TYPE] != Constants.STREAM_WRAPPER_CLASS_PATH:

                if not isinstance(value, Constants.TYPE_VS_DATATYPE.get(key_details[Constants.TYPE])):

                    detailsJO[Constants.FIELD] = name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.ACCEPTED_TYPE] = key_details[Constants.TYPE]

                    raise SDKException(Constants.TYPE_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

            if key_details.__contains__(Constants.VALUES):

                values_ja = key_details[Constants.VALUES]

                if value not in values_ja:

                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.ACCEPTED_VALUES] = values_ja

                    ex = SDKException(Constants.UNACCEPTED_VALUES_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

            if key_details.__contains__(Constants.UNIQUE):

                if key_details[Constants.UNIQUE]:

                    if name not in unique_values_map:

                        unique_values_map[name] = []

                    values_array = unique_values_map[name]

                    if value in values_array:

                        detailsJO[Constants.FIELD] = member_name

                        detailsJO[Constants.CLASS] = class_name

                        detailsJO[Constants.FIRST_INDEX] = values_array.index(value) + 1

                        detailsJO[Constants.NEXT_INDEX] = instance_number

                        ex = SDKException(Constants.UNIQUE_KEY_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                        Converter.logger.info(None, ex, exc_info=1)

                        raise ex

                    else:

                        unique_values_map[name].append(value)

            if key_details.__contains__(Constants.MIN_LENGTH) and key_details.__contains__(Constants.MAX_LENGTH):

                if len(str(value)) > key_details[Constants.MAX_LENGTH]:

                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.MAXIMUM_LENGTH] = key_details[Constants.MAX_LENGTH]

                    ex = SDKException(Constants.MAXIMUM_LENGTH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

                if len(str(value)) < key_details[Constants.MIN_LENGTH]:

                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.MINIMUM_LENGTH] = key_details[Constants.MIN_LENGTH]

                    ex = SDKException(Constants.MINIMUM_LENGTH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

            if key_details.__contains__(Constants.REGEX):

                if re.search(value, key_details[Constants.REGEX]) is None:

                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INSTANCE_NUMBER] = instance_number

                    raise SDKException(Constants.REGEX_MISMATCH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

            return True

        def get_record_json_file_path(self):

            """
            This method to get the module field JSON details file path.
            :return: A str representing the module field JSON details file path.
            """

            import src.com.zoho.crm.api.initializer as Init

            file_name = Init.Initializer.get_initializer().user.email

            file_name = file_name.split("@", 1)[0] + Init.Initializer.get_initializer().environment.url

            input_bytes = file_name.encode("UTF-8")

            encode_string = base64.b64encode(input_bytes)

            encode_string = str(encode_string.decode("UTF-8"))

            record_field_details_path = "/Users/raja-7453/Documents/AutomateSDK/python/GitLab/zohocrm-python-sdk/src/" + encode_string + ".json"

            return record_field_details_path
else:

    from abc import ABCMeta, abstractmethod

    class Converter:

        """
        This abstract class to use construct API request and response.
        """

        __metaclass__ = ABCMeta

        logger = logging.getLogger('client_lib')

        def __init__(self, common_api_handler):

            """
            Creates a Converter class instance with the CommonAPIHandler class instance.
            :param common_api_handler: A CommonAPIHandler class instance.
            """

            self.common_api_handler = common_api_handler

        @abstractmethod
        def get_response(self, response, pack):

            """
            This abstract method to process the API response.
            :param response: A object containing the API response contents or response.
            :param pack: A str containing the expected method return type.
            :return: A object representing the POJO class instance.
            """

            pass

        @abstractmethod
        def form_request(self, request_object, pack, instance_number):

            """
            This abstract method to construct the API request.
            :param request_object: A Object containing the POJO class instance.
            :param pack: A str containing the expected method return type.
            :param instance_number: An int containing the POJO class instance list number.
            :return: A object representing the API request body object.
            """

            pass

        @abstractmethod
        def append_to_request(self, request_base, request_object):

            """
            This abstract method to construct the API request body.
            :param request_base: A HttpEntityEnclosingRequestBase class instance.
            :param request_object: A object containing the API request body object.
            """

            pass

        @abstractmethod
        def get_wrapped_response(self, response, pack):

            """
           This abstract method to process the API response.
           :param response: A object containing the HttpResponse class instance.
           :param pack: A str containing the expected method return type.
           :return: A object representing the POJO class instance.
           """

            pass

        def value_checker(self, class_name, member_name, key_details, value, unique_values_map, instance_number):

            """
            This method is to validate if the input values satisfy the constraints for the respective fields.
            :param class_name: A str containing the class name.
            :param member_name: A str containing the member name.
            :param key_details: A JSON object containing the key JSON details.
            :param value: A object containing the key value.
            :param unique_values_map: A list containing the construct objects.
            :param instance_number: An int containing the POJO class instance list number.
            :return: A bool representing the key value is expected pattern, unique, length, and values.
            """

            from src.com.zoho.api.exception import SDKException

            from .constants import Constants

            detailsJO = {}

            name = key_details[Constants.NAME]

            # Data Type Validation
            if key_details[Constants.TYPE] != Constants.STREAM_WRAPPER_CLASS_PATH:

                if not isinstance(value, Constants.TYPE_VS_DATATYPE.get(key_details[Constants.TYPE])):

                    detailsJO[Constants.FIELD] = name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.ACCEPTED_TYPE] = key_details[Constants.TYPE]

                    raise SDKException(Constants.TYPE_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

            if key_details.__contains__(Constants.VALUES):

                values_ja = key_details[Constants.VALUES]

                if value not in values_ja:
                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.ACCEPTED_VALUES] = values_ja

                    ex = SDKException(Constants.UNACCEPTED_VALUES_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

            if key_details.__contains__(Constants.UNIQUE):

                if key_details[Constants.UNIQUE]:

                    if name not in unique_values_map:
                        unique_values_map[name] = []

                    values_array = unique_values_map[name]

                    if value in values_array:

                        detailsJO[Constants.FIELD] = member_name

                        detailsJO[Constants.CLASS] = class_name

                        detailsJO[Constants.FIRST_INDEX] = values_array.index(value) + 1

                        detailsJO[Constants.NEXT_INDEX] = instance_number

                        ex = SDKException(Constants.UNIQUE_KEY_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                        Converter.logger.info(None, ex, exc_info=1)

                        raise ex

                    else:

                        unique_values_map[name].append(value)

            if key_details.__contains__(Constants.MIN_LENGTH) and key_details.__contains__(Constants.MAX_LENGTH):

                if len(str(value)) > key_details[Constants.MAX_LENGTH]:

                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.MAXIMUM_LENGTH] = key_details[Constants.MAX_LENGTH]

                    ex = SDKException(Constants.MAXIMUM_LENGTH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

                if len(str(value)) < key_details[Constants.MIN_LENGTH]:
                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INDEX] = instance_number

                    detailsJO[Constants.MINIMUM_LENGTH] = key_details[Constants.MIN_LENGTH]

                    ex = SDKException(Constants.MINIMUM_LENGTH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

                    Converter.logger.info(None, ex, exc_info=1)

                    raise ex

            if key_details.__contains__(Constants.REGEX):

                if re.search(value, key_details[Constants.REGEX]) is None:
                    detailsJO[Constants.FIELD] = member_name

                    detailsJO[Constants.CLASS] = class_name

                    detailsJO[Constants.INSTANCE_NUMBER] = instance_number

                    raise SDKException(Constants.REGEX_MISMATCH_ERROR, None, details=detailsJO, cause=traceback.format_stack(limit=6))

            return True

        def get_record_json_file_path(self):

            """
            This method to get the module field JSON details file path.
            :return: A str representing the module field JSON details file path.
            """

            import src.com.zoho.crm.api.initializer as Init

            file_name = Init.Initializer.get_initializer().user.email

            file_name = file_name.split("@", 1)[0] + Init.Initializer.get_initializer().environment.url

            input_bytes = file_name.encode("UTF-8")

            encode_string = base64.b64encode(input_bytes)

            encode_string = str(encode_string.decode("UTF-8"))

            record_field_details_path = "/Users/raja-7453/Documents/AutomateSDK/python/GitLab/zohocrm-python-sdk/src/" + encode_string + ".json"

            return record_field_details_path
