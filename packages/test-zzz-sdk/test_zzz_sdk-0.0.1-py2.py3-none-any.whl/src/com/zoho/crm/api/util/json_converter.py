
try:

    from .converter import Converter

    from .constants import Constants

    from .datatype_converter import DataTypeConverter

    from src.com.zoho.api.exception.sdk_exception import SDKException

    import src.com.zoho.crm.api.initializer as Init

    from src.com.zoho.crm.api.util.utility import Utility

    import importlib

    import logging

    import re

    import traceback

    import json

except Exception:

    import importlib

    import traceback

    from .converter import Converter

    from .constants import Constants

    from .datatype_converter import DataTypeConverter

    from src.com.zoho.api.exception import SDKException

    import src.com.zoho.crm.api.initializer as Init

    from src.com.zoho.crm.api.util.utility import Utility

    import logging

    import re


class JSONConverter(Converter):

    """
    This class processes the API response object to the POJO object and POJO object to a JSON object.
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

        if class_json_details.keys().__contains__(Constants.INTERFACE) and class_json_details[Constants.INTERFACE] is not None:

            request_object_class_name = request_object.__class__.__module__

            request_object_class_name = str(request_object_class_name).replace("src.", "")

            path_split = str(request_object_class_name).rpartition(".")

            request_class_name = self.module_to_class(path_split[-1])

            request_object_class_name = path_split[0] + "." + request_class_name

            classes = class_json_details[Constants.CLASSES]

            for class_name in classes:

                class_name_interface_lower = str(class_name).lower()

                request_class_path_lower = request_object_class_name.lower()

                if class_name_interface_lower == request_class_path_lower:

                    class_json_details = dict(Initializer.json_details[str(class_name)])

                    break

        for member_name in class_json_details:

            member_json_details = class_json_details[member_name]

            if member_json_details.__contains__(Constants.READ_ONLY) or not member_json_details.__contains__(Constants.NAME):

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

            if value is not None and self.value_checker(class_name=class_name, member_name=member_name, key_details=member_json_details, value=field_value, unique_values_map=self.unique_dict, instance_number=instance_number) is True:

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

                    request[key_name] = DataTypeConverter.post_convert(field_value, type)

        if pack.__eq__(Constants.RECORD_NAMESPACE):

            record_field_details_path = self.get_record_json_file_path()

            with open(record_field_details_path, mode='r') as JSON:

                record_json_details = json.load(JSON)[self.common_api_handler.module_api_name]

            key_values = getattr(request_object, self.construct_private_member(class_name=class_name, member_name=Constants.KEY_VALUES))

            for key_name, key_json_detail in record_json_details.items():

                if key_values.__contains__(key_name):

                    if key_json_detail.__contains__(Constants.STRUCTURE_NAME):

                        key_value = self.form_request(key_values[key_name],key_json_detail[Constants.STRUCTURE_NAME], 1)

                    else:

                        key_value = self.redirector_for_object_to_json(key_values[key_name])

                    request[key_name] = key_value

        return request

    def append_to_request(self, request_base, request_object):

        return json.dumps(request_object).encode('utf-8')

    def set_json_object(self, field_value, member_json_details):

        json_object = {}

        if member_json_details is None:

            for key, value in field_value.items():

                json_object[key] = self.redirector_for_object_to_json(value)

        else:

            keys_detail = member_json_details[Constants.KEYS]

            for key_detail in keys_detail:

                key_value = None

                key_name = key_detail[Constants.NAME]

                if field_value.__contains__(key_name) and field_value[key_name] is not None:

                    if key_detail.__contains__(Constants.STRUCTURE_NAME):

                        key_value = self.form_request(field_value[key_name], key_detail[Constants.STRUCTURE_NAME], 1)

                    else:

                        key_value = self.redirector_for_object_to_json(field_value[key_name])

                    json_object[key_name] = key_value

        return json_object

    def set_json_array(self, field_value, member_json_details):

        json_array = []

        if member_json_details is None:

            for request in field_value:

                json_array.append(self.redirector_for_object_to_json(request))
        else:

            if member_json_details.__contains__(Constants.STRUCTURE_NAME):

                instance_count = 1

                pack = member_json_details[Constants.STRUCTURE_NAME]

                for request in field_value:

                    json_array.append(self.form_request(request, pack, instance_count))

                    instance_count += 1
            else:

                for request in field_value:

                    json_array.append(self.redirector_for_object_to_json(request))

        return json_array

    def redirector_for_object_to_json(self, request):

        if isinstance(request, list):

            return self.set_json_array(request, None)

        elif isinstance(request, dict):

            return self.set_json_object(request, None)

        else:

            return request

    def get_wrapped_response(self, response, pack):

        try:

            return self.get_response(response.json(), pack)

        except ValueError:

            return None

        return None

    def get_response(self, response, pack):

        try:

            from ..initializer import Initializer

        except Exception:

            from ..initializer import Initializer

        if response is None:

            return None

        response_json = dict(response)

        path_split = str(pack).rpartition(".")

        class_name = self.module_to_class(path_split[-1])

        pack = path_split[0] + "." + class_name

        record_json_details = dict(Initializer.json_details[str(pack)])

        instance = None

        if record_json_details.keys().__contains__(Constants.INTERFACE) and record_json_details[Constants.INTERFACE] is not None:

            classes = record_json_details[Constants.CLASSES]

            instance = self.find_match(classes, response_json)

        else:

            imported_module = importlib.import_module(path_split[0])

            class_holder = getattr(imported_module, class_name)

            instance = class_holder()

            for member_name, member_json_details in record_json_details.items():

                key_name = member_json_details[Constants.NAME] if Constants.NAME in member_json_details else None

                if key_name is not None and response_json.__contains__(key_name) and response_json.get(key_name) is not None:

                    key_data = response_json.get(key_name)

                    type = member_json_details[Constants.TYPE]

                    instance_value = None

                    if type == Constants.LIST:

                        instance_value = []

                        instance_value = self.get_collections_data(key_data, member_json_details)

                    elif type == Constants.MAP:

                        instance_value = {}

                        instance_value = self.get_map_data(key_data, member_json_details)

                    elif member_json_details.__contains__(Constants.STRUCTURE_NAME):

                        instance_value = self.get_response(key_data, member_json_details[Constants.STRUCTURE_NAME])

                    else:

                        instance_value = DataTypeConverter.pre_convert(key_data, type)

                    setattr(instance, self.construct_private_member(class_name=class_name, member_name=member_name), instance_value)

            if pack.__eq__(Constants.RECORD_NAMESPACE):

                record_field_details_path = self.get_record_json_file_path()

                with open(record_field_details_path, mode='r') as JSON:

                    module_json_details = None

                    if self.common_api_handler.module_api_name is not None:

                        module_json_details = json.load(JSON)[self.common_api_handler.module_api_name]

                instance_value = {}

                if module_json_details is not None:

                    for key_name, key_json_details in module_json_details.items():

                        field_name = key_name.lower()

                        if not record_json_details.__contains__(field_name):

                            if response_json.__contains__(key_name):

                                key_value = None

                                if key_json_details.__contains__(Constants.STRUCTURE_NAME):

                                    key_value = self.get_response(response_json[key_name], key_json_details[Constants.STRUCTURE_NAME])

                                else:

                                    key_value = self.redirector_for_json_to_object(response_json[key_name])

                                instance_value[key_name] = key_value
                else:

                    for json_key_name, key_value in response_json.items():

                        key_name = json_key_name.lower()

                        if not record_json_details.__contains__(key_name):

                            instance_value[json_key_name] = key_value

                setattr(instance, self.construct_private_member(class_name=class_name, member_name=Constants.KEY_VALUES), instance_value)

        return instance

    def get_map_data(self, key_data, member_json_details):

        map_instance = {}

        responses = key_data

        if member_json_details is None:

            for key, response in responses.items():

                map_instance[key] = response

        else:

            keys_detail = member_json_details[Constants.KEYS]

            for key_detail in keys_detail:

                key_name = key_detail[Constants.NAME]

                key_value = None

                if responses.__contains__(key_name) and responses[key_name] is not None:

                    if key_detail.__contains__(Constants.STRUCTURE_NAME):

                        key_value = self.get_response(responses[key_name], key_detail[Constants.STRUCTURE_NAME])

                        map_instance[key_name] = key_value

                    else:

                        key_value = responses[key_name]

                        map_instance[key_name] = self.redirector_for_json_to_object(key_value)

        return map_instance

    def get_collections_data(self, key_data, member_json_details):

        values = []

        responses = key_data

        if member_json_details is None:

            for response in responses:

                values.append(self.redirector_for_json_to_object(response))

        else:

            if member_json_details.__contains__(Constants.STRUCTURE_NAME):

                pack = member_json_details[Constants.STRUCTURE_NAME]

                for response in responses:

                    values.append(self.get_response(response, pack))

            else:

                for response in responses:

                    values.append(self.redirector_for_json_to_object(response))

        return values

    def redirector_for_json_to_object(self, key_data):

        if isinstance(key_data, dict):

            return self.get_map_data(key_data, None)

        elif isinstance(key_data, list):

            return self.get_collections_data(key_data, None)

        else:

            return key_data

    def find_match(self, classes, response_json):

        pack = ""

        ratio = 0

        for class_name in classes:

            match_ratio = self.find_ratio(class_name, response_json)

            if match_ratio == 1.0:

                pack = class_name

                ratio = 1

                break

            elif match_ratio > ratio:

                ratio = match_ratio

                pack = class_name

        return self.get_response(response_json, pack)

    def find_ratio(self, class_name, response_json):

        try:

            from ..initializer import Initializer

        except Exception:

            from ..initializer import Initializer

        class_json_details = dict(Initializer.json_details[str(class_name)])

        total_points = len(class_json_details.keys())

        matches = 0

        if total_points == 0:

            return

        else:

            for member_name in class_json_details:

                member_json_details = class_json_details[member_name]

                key_name = member_json_details[Constants.NAME] if Constants.NAME in member_json_details else None

                if key_name is not None and response_json.__contains__(key_name) and response_json.get(key_name) is not None:

                    key_data = response_json[key_name]

                    type = type(key_data).__name__

                    if isinstance(key_data, int):

                        type = "Integer"

                    if isinstance(key_data, bool):

                        type = "Boolean"

                    if isinstance(key_data, str):

                        type = "String"

                    if isinstance(key_data, dict):

                        type = "Map"

                    if isinstance(key_data, list):

                        type = "List"

                    if type == member_json_details[Constants.TYPE]:

                        if member_json_details.__contains__(Constants.VALUES):

                            for value in member_json_details[Constants.VALUES]:

                                if value == key_data:

                                    matches += 1

                                    break

                        else:

                            matches += 1

        return matches / total_points

    def construct_private_member(self, class_name, member_name):

        return '_' + class_name + '__' + member_name
