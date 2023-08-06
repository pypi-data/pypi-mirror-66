
try:

    from .converter import Converter

    from .constants import Constants

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

    import logging

    import re


class Downloader(Converter):

    """
    This class to process the download file and stream response.
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

        return None

    def append_to_request(self, request_base, request_object):

        return

    def get_wrapped_response(self, response, pack):

        return self.get_response(response, pack)

    def get_response(self, response, pack):

        try:
            from ..initializer import Initializer

        except Exception:

            from ..initializer import Initializer

        path_split = str(pack).rpartition(".")

        class_name = self.module_to_class(path_split[-1])

        pack = path_split[0] + "." + class_name

        class_json_details = dict(Initializer.json_details[str(pack)])

        instance = self.get_class_instance(class_name, path_split[0])()

        for member_name, member_json_details in class_json_details.items():

            member_name = member_json_details[Constants.NAME] if Constants.NAME in member_json_details else None

            if member_name is not None:

                type = member_json_details[Constants.TYPE]

                instance_value = None

                if type == Constants.STREAM_WRAPPER_CLASS_PATH:

                    file_name = ''

                    content_disposition = response.headers[Constants.CONTENT_DISPOSITION]

                    if "'" in content_disposition:

                        start_index = content_disposition.rindex("'")

                        file_name = content_disposition[start_index + 1:]

                    elif '"' in content_disposition:

                        start_index = content_disposition.rindex('=')

                        file_name = content_disposition[start_index + 1:].replace('"', '')

                    stream_path_split = str(type).rpartition(".")

                    stream_class_name = self.module_to_class(stream_path_split[-1])

                    instance_value = self.get_class_instance(stream_class_name, stream_path_split[0])(None, file_name, response)

                setattr(instance, self.construct_private_member(class_name=class_name, member_name=member_name), instance_value)

        return instance

    def construct_private_member(self, class_name, member_name):

        return '_' + class_name + '__' + member_name

    def get_class_instance(self, class_name, class_path):

        imported_module = importlib.import_module(class_path)

        class_holder = getattr(imported_module, class_name)

        return class_holder
