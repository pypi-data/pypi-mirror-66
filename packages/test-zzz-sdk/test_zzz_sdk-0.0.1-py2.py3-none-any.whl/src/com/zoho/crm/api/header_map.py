
class HeaderMap(object):

    """
    This class representing the HTTP header name and value.
    """

    def __init__(self):

        self.header_map = dict()

    def add(self, header, value):

        """
        This method to add header name and value.
        :param header: A Header class instance.
        :param value: A object containing the header value.
        """

        name = header.name

        value_list = []

        if not self.header_map.__contains__(name):

            value_list.append(value)

            self.header_map[name] = value_list

        else:

            value_list = self.header_map[name]

            value_list.append(value)

            self.header_map[name] = value_list
