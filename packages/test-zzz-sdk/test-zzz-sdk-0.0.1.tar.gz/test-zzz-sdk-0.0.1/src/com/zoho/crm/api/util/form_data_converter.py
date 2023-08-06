
try:

    from .converter import Converter

    from .constants import Constants

    import importlib

    import logging

    import re

    import traceback

    import json

    from src.com.zoho.api.exception.sdk_exception import SDKException

except Exception:

    import importlib

    import traceback

    import logging

    import re

    from .converter import Converter

    from .constants import Constants

    from src.com.zoho.api.exception import SDKException


class FormDataConverter(Converter):

    """
    This class to process the upload file and stream.
    """

    logger = logging.getLogger('client_lib')

    def __init__(self, common_api_handler):

        self.unique_dict = {}

        self.count = 0

        self.common_api_handler = common_api_handler

    def module_to_class(self, module_name):

        class_name = module_name

        if "_" in module_name:

            class_name = ''

            module_split = str(module_name).split('_')

            for each_name in module_split:

                each_name = each_name.capitalize()

                class_name += each_name

        return class_name

    def form_request(self, request_object, pack, instance_number):

        pack = str(pack).replace("src.", "")

        path_split = str(pack).rpartition(".")

        class_name = self.module_to_class(path_split[-1])

        pack = path_split[0] + "." + class_name

        try:

            from ..initializer import Initializer

        except Exception:

            from ..initializer import Initializer

        class_json_details = dict(Initializer.json_details[str(pack)])

        request = dict()

        for member_name in class_json_details:

            member_json_details = class_json_details[member_name]

            if (member_json_details.__contains__(Constants.READ_ONLY) and bool(member_json_details[Constants.READ_ONLY])) or not member_json_details.__contains__(Constants.NAME):

                continue

            value = getattr(request_object, Constants.IS_KEY_MODIFIED)(member_name)

            if value is None and member_json_details.__contains__(Constants.REQUIRED) and bool(member_json_details[Constants.REQUIRED]):

                error = {

                    Constants.INDEX: instance_number,

                    Constants.CLASS: class_name,

                    Constants.FIELD: member_name
                }

                raise SDKException(Constants.MANDATORY_VALUE_MISSING_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            field_value = getattr(request_object, self.construct_private_member(class_name=class_name, member_name=member_name))

            if value is not None:

                getattr(request_object, Constants.SET_KEY_MODIFIED)(0, member_name)

                key_name = member_json_details.get(Constants.NAME)

                type = member_json_details.get(Constants.TYPE)

                if type == Constants.LIST:

                    request[key_name] = self.set_json_array(field_value, member_json_details)

                elif type == Constants.MAP or type == Constants.HASH_MAP:

                    request[key_name] = self.set_json_object(field_value, member_json_details)

                elif member_json_details.__contains__(Constants.STRUCTURE_NAME):

                    request[key_name] = self.form_request(field_value, member_json_details.get(Constants.STRUCTURE_NAME), 1)

                else:

                    request[key_name] = field_value

            return request

    def append_to_request(self, request_base, request_object):

        request_file_stream = {}

        for key_name, key_value in request_object.items():

            request_file_stream[key_name] = key_value.get_stream()

        request_base.file = True

        return request_file_stream

    def set_json_object(self, field_value, member_json_details):

        json_object = {}

        if member_json_details is None:

            for key, value in field_value.items():

                json_object[key] = self.re_director_for_object_to_json(value)
        else:

            keys_detail = member_json_details[Constants.KEYS]

            for key_detail in keys_detail:

                key_name = key_detail[Constants.NAME]

                key_value = None

                if field_value.__contains__(key_name) and field_value[key_name] is not None:

                    if key_detail.__contains__(Constants.STRUCTURE_NAME):

                        key_value = self.form_request(field_value[key_name], key_detail[Constants.STRUCTURE_NAME], 1)

                    else:

                        key_value = self.re_director_for_object_to_json(field_value[key_name])

                    json_object[key_name] = key_value

        return json_object

    def set_json_array(self, field_value, member_json_details):

        json_array = []

        if member_json_details is None:

            for value in field_value:

                json_array.append(self.re_director_for_object_to_json(value))
        else:

            if member_json_details.__contains__(Constants.STRUCTURE_NAME):

                instance_count = 1

                pack = member_json_details[Constants.STRUCTURE_NAME]

                for request in field_value:

                    json_array.append(self.form_request(request, pack, instance_count))

                    instance_count += 1
            else:

                for request in field_value:

                    json_array.append(self.re_director_for_object_to_json(request))

        return json_array

    def re_director_for_object_to_json(self, request):

        if isinstance(request, list):

            return self.set_json_array(request, None)

        if isinstance(request, dict):

            return self.set_json_object(request, None)

        else:

            return request

    def get_wrapped_response(self, response, pack):

        return None

    def get_response(self, response, pack):

        return None

    def construct_private_member(self, class_name, member_name):

        return '_' + class_name + '__' + member_name
