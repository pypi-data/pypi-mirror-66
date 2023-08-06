
class APIResponse(object):

    """
    This class is the common API response object.
    """

    def __init__(self, headers, status_code, data_object):

        """
        Creates an APIResponse class instance with the specified parameters.
        :param headers: A dict containing the API response headers.
        :param status_code: A int containing the API response HTTP status code.
        :param data_object: A object containing the API response POJO class instance.
        """

        self.headers = headers

        self.status_code = status_code

        self.data_object = data_object

    def get_headers(self):

        """
        This is a getter method to get API response headers.
        :return: A dict representing the API response headers.
        """

        return self.headers

    def get_status_code(self):

        """
        This is a getter method to get the API response HTTP status code.
        :return: A int representing the API response HTTP status code.
        """

        return self.status_code

    def get_data_object(self):

        """
        This method to get an API response POJO class instance.
        :return: A POJO class instance.
        """

        return self.data_object
