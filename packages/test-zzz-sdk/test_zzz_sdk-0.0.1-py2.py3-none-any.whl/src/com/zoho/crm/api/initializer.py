
try:

    import logging

    import os

    import json

    import traceback

    import threading

    from src.com.zoho.api.authenticator.store.token_store import TokenStore

    from src.com.zoho.api.exception.sdk_exception import SDKException

    from src.com.zoho.crm.api.user import User

    from src.com.zoho.crm.api.dc.data_center import DataCenter

    from src.com.zoho.crm.api.util.constants import Constants

except Exception:

    import logging

    import os

    import json

    import traceback

    import threading

    from ...api.authenticator.store.token_store import TokenStore

    from ...api.exception.sdk_exception import SDKException

    from ..api.user import User

    from ..api.dc.data_center import DataCenter

    from ..api.util.constants import Constants


class Initializer(object):

    """
    This class to initialize Zoho CRM SDK.
    """

    logger = logging.getLogger('client_lib')

    json_details = None

    environment = None

    user = None

    store = None

    token = None

    initializer = None

    LOCAL = threading.local()

    LOCAL.init = None

    @classmethod
    def initialize(cls, user, environment, token, store, logger=None):

        """
        This to initialize the SDK.
        :param user: A User class instance represents the CRM user.
        :param environment: A Environment class instance containing the CRM API base URL and Accounts URL.
        :param token: A Token class instance containing the OAuth client application information.
        :param store: A TokenStore class instance containing the token store information.
        :param logger: A Logger class instance containing the log file path and Logger type.
        """

        error = {}

        try:

            from .logger import Logger, SDKLogger

        except Exception:

            from src.com.zoho.crm.api.logger import Logger, SDKLogger

        if logger is not None:

            SDKLogger.initialize(logger.level, logger.file_path)

        else:

            SDKLogger.initialize(Logger.Levels.INFO, os.path.join(os.getcwd(), Constants.LOGFILE_NAME))

        try:

            from src.com.zoho.api.authenticator.token import Token

            if not isinstance(user, User):

                error[Constants.FIELD] = Constants.USER

                error[Constants.EXPECTED_TYPE] = User.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(environment, DataCenter.Environment):

                error[Constants.FIELD] = Constants.ENVIRONMENT

                error[Constants.EXPECTED_TYPE] = DataCenter.Environment.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(store, TokenStore):

                error[Constants.FIELD] = Constants.STORE

                error[Constants.EXPECTED_TYPE] = TokenStore.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            if not isinstance(token, Token):

                error[Constants.FIELD] = Constants.TOKEN

                error[Constants.EXPECTED_TYPE] = Token.__name__

                raise SDKException(Constants.INITIALIZATION_ERROR, None, details=error, cause=traceback.format_stack(limit=6))

            cls.environment = environment

            cls.user = user

            cls.token = token

            cls.store = store

            cls.initializer = cls

        except SDKException as e:

            cls.logger.error(Constants.INITIALIZATION_ERROR + e.__str__())

        dir_name = os.path.dirname(__file__)

        filename = os.path.join(dir_name, '..', '..', '..', '..', Constants.JSON_DETAILS_FILE_PATH)

        with open(filename, mode='r') as JSON:

            cls.json_details = json.load(JSON)

    @classmethod
    def get_initializer(cls):

        """
        This method to get Initializer class instance.
        :return: A Initializer class instance representing the SDK configuration details.
        """

        if Initializer.LOCAL.init is not None:

            return Initializer.LOCAL.init

        return cls.initializer

    @classmethod
    def switch_user(cls, user, environment, token):

        """
        This method to switch the different user in SDK environment.
        :param user: A User class instance represents the CRM user.
        :param environment: A Environment class instance containing the CRM API base URL and Accounts URL.
        :param token: A Token class instance containing the OAuth client application information.
        """

        cls.user = user

        cls.environment = environment

        cls.token = token

        cls.store = Initializer.initializer.store

        Initializer.LOCAL.init = cls.initializer

