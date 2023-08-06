import src.com.zoho.crm.api.logger.log as logger_file
import src.com.zoho.crm.api.logger
import src.com.zoho.crm.api.dc as DC
import src.com.zoho.crm.api.user as User
import src.com.zoho.api.authenticator.store.file_store as FileStore
import src.com.zoho.api.authenticator.oauth_token as OAuthToken
import src.com.zoho.crm.api.initializer as Init
import src.com.zoho.crm.api.contact_roles as ContactRoles
import src.com.zoho.crm.api.record as Record
import src.com.zoho.api.authenticator.store.db_store as DBStore

import src.com.zoho.crm.api.record.file_body_wrapper as FileBodyWrapper

import src.com.zoho.crm.api.util.stream_wrapper as StreamWrapper
from src.com.zoho.crm.api.record.field import Field as Field

# regex = '^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$

class Test(object):
    def test(self):
        # log_instance = logger_file.Log.get_instance(logger_file.Log.Levels.INFO, '/Users/pravesh-8541/sdk.log')
        environment = DC.USDataCenter.PRODUCTION()
        user = User.User('raja.k@zohocorp.com')
        store = DBStore.DBStore(None, None, None, "raja@7453", None)
        # store = FileStore.FileStore("/Users/visali-pttk3214/sdkProjects/python/zohocrm-python-sdk/src/file.txt")
        token = OAuthToken.OauthToken("1000.1RGSB1XEI2FVG0TYVWPZ864L7KI3DH",
                                      "550045e5e5a4722aa39326e3af819c84683f94cb2a",
                                      "https://www.zoho.com",
                                      "1000.b632a2d7439abfd8b50147886b8a2f41.6547e4cba91550e5006de16da7fc2401",
                                      OAuthToken.TokenType.refresh)

        Init.Initializer.initialize(user, environment, token, store, None)

        # ro = Record.RecordOperations("Leads").get_records()#get_attachments(3477061000004996185)
        # print(ro.__dict__)

        # bo = FileBodyWrapper.FileBodyWrapper()
        #
        # file_stream = StreamWrapper.StreamWrapper("/Users/raja-7453/Desktop/test/photo.png")
        #
        # bo.set_file(file_stream)

        # upload = Record.RecordOperations("Leads").upload_attachments(bo, "3477061000004996185")
        #
        # print(upload.status_code)

        download = Record.RecordOperations("Leads").get_records();#download_attachment("3477061000004996185", "347706100000525200")

        # print(download.status_code)
        # common_response = download.get_data_object()
        # streamWrapper = common_response.get_file()

        # with open('/Users/raja-7453/Documents/AutomateSDK/python/' + streamWrapper.get_name(), 'wb') as f:
        #     for chunk in streamWrapper.get_stream():
        #         f.write(chunk)
        # f.close()

        # date = DataTypeConverter.DataTypeConverter.pre_convert("2013-02-19T10:00:00+05:00", "Date")
        #
        # date1= DataTypeConverter.DataTypeConverter.post_convert(date, "Date")

        # bw = Record.BodyWrapper()
        # data = ro.get_data()
        # data[0].get_key_values()["Owner"].set_id("asd")
        # bw.set_data(data)
        # re = Record.RecordOperations("Leads").create_records(bw)



name = Test()
name.test()