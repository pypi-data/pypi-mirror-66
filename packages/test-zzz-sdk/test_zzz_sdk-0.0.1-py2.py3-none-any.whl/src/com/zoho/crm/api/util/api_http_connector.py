
from .constants import Constants

import requests


class APIHTTPConnector(object):

    """
    This module is to make HTTP connections, trigger the requests and receive the response.
    """

    def __init__(self):

        """
        Creates an APIHTTPConnector class instance with the specified parameters.
        """

        self.url = None

        self.headers = dict()

        self.req_method = None

        self.params = dict()

        self.req_body = None

        self.file = False

    def fire_request(self, convert_instance):

        """
        This method makes a request to the Zoho CRM Rest API
        :param convert_instance: A Converter class instance to call appendToRequest method.
        :return: Response object or None
        """

        response = None

        if self.req_method == Constants.REQUEST_METHOD_GET:

            response = requests.get(self.url, headers=self.headers, params=self.params, allow_redirects=False)

        elif self.req_method == Constants.REQUEST_METHOD_PUT:

            data = convert_instance.append_to_request(self, self.req_body)

            response = requests.put(self.url, data=data, params=self.params, headers=self.headers, allow_redirects=False)

        elif self.req_method == Constants.REQUEST_METHOD_POST:

            data = convert_instance.append_to_request(self, self.req_body)

            if self.file is False:

                response = requests.post(self.url, data=data, params=self.params, headers=self.headers, allow_redirects=False)

            else:

                response = requests.post(self.url, files=data, headers=self.headers, allow_redirects=False, data={})

        elif self.req_method == Constants.REQUEST_METHOD_DELETE:

            response = requests.delete(self.url, headers=self.headers, params=self.params, allow_redirects=False)

        return response
