
try:

    from abc import abstractmethod,  ABC

    import sys

except Exception as e:

    from abc import abstractmethod, ABCMeta

    import sys

if sys.version_info[0] < 3:

    class DataCenter:

        """
        This abstract class representing the Zoho CRM environment and accounts URL.
        """

        __metaclass__ = ABCMeta

        @abstractmethod
        def get_iam_url(self):

            """
            This method to get accounts URL.
            :return: A str representing the accounts URL.
            """

            pass

        class Environment(object):

            """
            This abstract class representing the Zoho CRM environment.
            """

            def __init__(self, url, accounts_url):

                """
                Creates an Environment class instance with the specified parameters.
                :param url: A str representing the Zoho CRM API URL.
                :param accounts_url: A str representing the accounts URL.
                """

                self.url = url

                self.accounts_url = accounts_url

                return

else:

    class DataCenter(ABC):

        """
        This abstract class representing the Zoho CRM environment and accounts URL.
        """


        @abstractmethod
        def get_iam_url(self):

            """
            This method to get accounts URL.
            :return: A str representing the accounts URL.
            """

            pass

        class Environment(object):

            def __init__(self, url, accounts_url):

                """
                Creates an Environment class instance with the specified parameters.
                :param url: A str representing the Zoho CRM API URL.
                :param accounts_url: A str representing the accounts URL.
                """

                self.url = url

                self.accounts_url = accounts_url

                return
