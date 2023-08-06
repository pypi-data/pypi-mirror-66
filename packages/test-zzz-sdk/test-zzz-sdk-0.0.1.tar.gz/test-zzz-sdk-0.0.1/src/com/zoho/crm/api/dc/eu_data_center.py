
try:

    from source.dc.data_center import DataCenter

except Exception as e:

    from .data_center import DataCenter


class EUDataCenter(DataCenter):

    """
    This class representing the European countries Zoho CRM and Accounts URL. It is used to denote the domain of the user.
    """

    @classmethod
    def PRODUCTION(cls):

        """
        This Environment class instance represents the European countries Zoho CRM production environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://www.zohoapis.eu", cls().get_iam_url())

    @classmethod
    def SANDBOX(cls):

        """
        This Environment class instance represents the European countries Zoho CRM sandbox environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://sandbox.zohoapis.eu", cls().get_iam_url())

    @classmethod
    def DEVELOPER(cls):

        """
        This Environment class instance represents the European countries Zoho CRM developer environment.
        :return:  A Environment class instance.
        """

        return DataCenter.Environment("https://developer.zohoapis.eu", cls().get_iam_url())

    def get_iam_url(self):

        """
        This method to get accounts URL.
        :return: A str representing the accounts URL.
        """

        return "https://accounts.zoho.eu/oauth/v2/token"
