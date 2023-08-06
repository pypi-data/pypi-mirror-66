
try:

    from source.dc.data_center import DataCenter

except Exception as e:

    from .data_center import DataCenter


class AUDataCenter(DataCenter):

    """
    This class representing the Australian country Zoho CRM and Accounts URL. It is used to denote the domain of the user.
    """

    @classmethod
    def PRODUCTION(cls):

        """
        This Environment class instance represents the Australian country's Zoho CRM production environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://www.zohoapis.com.au", cls().get_iam_url())

    @classmethod
    def SANDBOX(cls):

        """
        This Environment class instance represents the Australian country's Zoho CRM sandbox environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://sandbox.zohoapis.com.au", cls(). get_iam_url())

    @classmethod
    def DEVELOPER(cls):

        """
        This Environment class instance represents the Australian country's Zoho CRM developer environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://developer.zohoapis.com.au", cls(). get_iam_url())

    def get_iam_url(self):

        """
        This method to get accounts URL.
        :return: A str representing the accounts URL.
        """

        return "https://accounts.zoho.com.au/oauth/v2/token"
