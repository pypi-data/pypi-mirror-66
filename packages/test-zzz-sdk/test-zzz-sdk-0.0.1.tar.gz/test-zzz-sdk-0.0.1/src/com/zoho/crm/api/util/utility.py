
try:

    import logging

    import os

    import json

    import src.com.zoho.crm.api.fields as Field

    import zlib

    import base64

    import re

    from .constants import Constants

except Exception:

    import logging

    import os

    import json

    import zlib

    import base64

    import re

    from .constants import Constants


class Utility(object):

    """
    This class handles module field details.
    """

    @staticmethod
    def get_fields(module_api_name):

        """
        This method to fetch field details of the current module for the current user and store the result in a JSON file.
        :param module_api_name: A str containing the CRM module API name.
        """

        import src.com.zoho.crm.api.initializer as Init

        file_name = Init.Initializer.get_initializer().user.email

        file_name = file_name.split("@", 1)[0] + Init.Initializer.get_initializer().environment.url

        input_bytes = file_name.encode("UTF-8")

        encode_string = base64.b64encode(input_bytes)

        encode_string = str(encode_string.decode("UTF-8"))

        record_field_details_path = "/Users/raja-7453/Documents/AutomateSDK/python/GitLab/zohocrm-python-sdk/src/" + encode_string + ".json"

        if os.path.exists(record_field_details_path):

            with open(record_field_details_path, mode="r") as JSON:

                record_field_details_json = json.load(JSON)

                JSON.close()

                if record_field_details_json.__contains__(module_api_name):

                    return

            with open(record_field_details_path, mode="w") as JSON:

                record_field_details_json[module_api_name] = Utility.get_fields_details(module_api_name)

                json.dump(record_field_details_json, JSON)

        else:

            with open(record_field_details_path, mode='w') as JSON:

                record_field_details_json = {}

                record_field_details_json[module_api_name] = Utility.get_fields_details(module_api_name)

                json.dump(record_field_details_json, JSON)

    @staticmethod
    def get_fields_details(module_api_name):

        """
        This method to get module field data from Zoho CRM.
        :param module_api_name: A str containing the CRM module API name.
        :return: A object representing the Zoho CRM module field details.
        """

        fields = Field.FieldsOperations(module_api_name).get_fields().data_object.get_fields()

        fields_details = {}

        for field in fields:

            field_detail = {}

            Utility.set_data_type(field_detail, field)

            fields_details[field.get_api_name()] = field_detail

        return fields_details

    @staticmethod
    def set_data_type(field_detail, field):

        data_type = field.get_data_type()

        structure_name = None

        key_name = field.get_api_name()

        if data_type == "text" or data_type == "textarea" or data_type == "picklist" or data_type == "email" or data_type == "website" or data_type == "phone":

            data_type = "String"

        elif data_type == "fileupload" or data_type == "profileimage":

            data_type = "File"

        elif data_type == "boolean":

            data_type = "Boolean"

        elif data_type == "ownerlookup":

            structure_name = "com.zoho.crm.api.record.User"

            data_type = "com.zoho.crm.api.record.Record"

        elif data_type == "currency"or data_type == "double":

            data_type = "Double"

        elif data_type == "integer":

            data_type = "integer"

        elif data_type == "datetime":

            data_type = "LocalDateTime"

        elif data_type == "date":

            data_type = "LocalDate"

        elif data_type == "multiselectpicklist":

            data_type = "arrayList<String>"

        elif data_type == "datetime":

            data_type = "LocalDateTime"

        elif data_type == "bigint":

            data_type = "Long"

        elif data_type == "lookup":

            structure_name = "com.zoho.crm.api.record.Record"

            data_type = "com.zoho.crm.api.record.Record"

        elif data_type == "multiselectlookup":

            data_type = "ArrayList<Record>"

        field_detail[Constants.NAME] = key_name

        field_detail[Constants.TYPE] = data_type

        if structure_name:

            field_detail[Constants.STRUCTURE_NAME] = structure_name
