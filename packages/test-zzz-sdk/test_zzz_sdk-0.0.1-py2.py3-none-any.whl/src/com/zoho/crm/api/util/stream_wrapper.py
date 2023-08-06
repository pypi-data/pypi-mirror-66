
import os


class StreamWrapper(object):

    """
    This class handles the file stream and name.
    """

    def __init__(self, file_path, name=None, stream=None):

        """
        Creates a StreamWrapper class instance with the specified parameters.
        :param file_path: A str containing the file path.
        :param name: A str containing the file name.
        :param stream: A stream containing the file stream.
        """

        if file_path is not None:

            self.name = os.path.basename(file_path)

            self.stream = open(file_path, 'rb')

        else:

            self.name = name

            self.stream = stream

    def get_name(self):

        """
        This is a getter method to get the file name.
        :return: A str representing the file name.
        """

        return self.name

    def get_stream(self):

        """
        This is a getter method to get the file input stream.
        :return: A stream representing the file input stream.
        """

        return self.stream
