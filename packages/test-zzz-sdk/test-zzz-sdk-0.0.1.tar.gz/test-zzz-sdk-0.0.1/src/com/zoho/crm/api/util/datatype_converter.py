
from datetime import datetime

from dateutil.tz import tz


class DataTypeConverter(object):

    """
    This class converts JSON value to the expected data type.
    """

    pre_converter_map = {}

    post_converter_map = {}

    @staticmethod
    def init():

        """
        This method to initialize the PreConverter and PostConverter lambda functions.
        """

        if len(DataTypeConverter.pre_converter_map) != 0 and len(DataTypeConverter.post_converter_map) != 0:

            return

        DataTypeConverter.add_to_map("String", lambda obj: str(obj), lambda obj: str(obj))

        DataTypeConverter.add_to_map("Integer", lambda obj: int(obj), lambda obj: int(obj))

        DataTypeConverter.add_to_map("Long", lambda obj: str(obj), lambda obj: str(obj))

        DataTypeConverter.add_to_map("Boolean", lambda obj: bool(obj), lambda obj: bool(obj))

        DataTypeConverter.add_to_map("DateTime", lambda obj: datetime.fromisoformat(obj).astimezone(tz.tzlocal()), lambda obj: obj.isoformat())

    @staticmethod
    def add_to_map(name, pre_converter, post_converter):

        """
        This method to add PreConverter and PostConverter instance.
        :param name: A str containing the data type class name.
        :param pre_converter: A pre_converter interface.
        :param post_converter: A post_converter interface.
        """

        DataTypeConverter.pre_converter_map[name] = pre_converter

        DataTypeConverter.post_converter_map[name] = post_converter

    @staticmethod
    def pre_convert(obj, type):

        """
        This method to convert JSON value to expected data value.
        :param obj: A object containing the JSON value.
        :param type: A str containing the expected method return type.
        :return: A object containing the expected data value.
        """

        DataTypeConverter.init()

        return DataTypeConverter.pre_converter_map[type](obj)

    @staticmethod
    def post_convert(obj, type):

        """
        This method to convert python data to JSON data value.
        :param obj: A object containing the python data value.
        :param type: A str containing the expected method return type.
        :return: A object containing the expected data value.
        """

        DataTypeConverter.init()

        return DataTypeConverter.post_converter_map[type](obj)
