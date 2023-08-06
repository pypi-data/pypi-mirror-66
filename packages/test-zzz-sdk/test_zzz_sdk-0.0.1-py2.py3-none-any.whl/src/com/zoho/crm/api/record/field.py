class Field(object):
    def __init__(self,api_name):
        self.__api_name = api_name

    def get_API_name(self):
        return self.__api_name

    class Leads(object):
        @classmethod
        def owner(cls):
            return Field("Owner")

        @classmethod
        def company(cls):
            return Field("Company")

        @classmethod
        def last_name(cls):
            return Field("Last_Name")

        @classmethod
        def first_name(cls):
            return Field("First_Name")

        @classmethod
        def salutation(cls):
            return Field("Salutation")

        @classmethod
        def email(cls):
            return Field("Email")

        @classmethod
        def mobile(cls):
            return Field("Mobile")

        @classmethod
        def full_name(cls):
            return Field("Full_Name")

        @classmethod
        def phone(cls):
            return Field("Phone")

        @classmethod
        def lead_status(cls):
            return Field("Lead_Status")

        @classmethod
        def multi_select_1(cls):
            return Field("Multi_Select_1")

        @classmethod
        def industry(cls):
            return Field("Industry")

        @classmethod
        def currency(cls):
            return Field("Currency")

        @classmethod
        def rating(cls):
            return Field("Rating")

        @classmethod
        def file(cls):
            return Field("file")

        @classmethod
        def fax(cls):
            return Field("Fax")

        @classmethod
        def designation(cls):
            return Field("Designation")

        @classmethod
        def website(cls):
            return Field("Website")

        @classmethod
        def no_of_employees(cls):
            return Field("No_of_Employees")

        @classmethod
        def tag(cls):
            return Field("Tag")

        @classmethod
        def created_by(cls):
            return Field("Created_By")

        @classmethod
        def lead_source(cls):
            return Field("Lead_Source")

        @classmethod
        def skype_id(cls):
            return Field("Skype_ID")

        @classmethod
        def created_time(cls):
            return Field("Created_Time")

        @classmethod
        def secondary_email(cls):
            return Field("Secondary_Email")

        @classmethod
        def annual_revenue(cls):
            return Field("Annual_Revenue")

        @classmethod
        def modified_time(cls):
            return Field("Modified_Time")

        @classmethod
        def twitter(cls):
            return Field("Twitter")

        @classmethod
        def email_opt_out(cls):
            return Field("Email_Opt_Out")

        @classmethod
        def modified_by(cls):
            return Field("Modified_By")

        @classmethod
        def last_activity_time(cls):
            return Field("Last_Activity_Time")

        @classmethod
        def yes(cls):
            return Field("yes")

        @classmethod
        def exchange_rate(cls):
            return Field("Exchange_Rate")

        @classmethod
        def converted_date_time(cls):
            return Field("Converted_Date_Time")

        @classmethod
        def is_record_duplicate(cls):
            return Field("Is_Record_Duplicate")

        @classmethod
        def street(cls):
            return Field("Street")

        @classmethod
        def city(cls):
            return Field("City")

        @classmethod
        def state(cls):
            return Field("State")

        @classmethod
        def zip_code(cls):
            return Field("Zip_Code")

        @classmethod
        def country(cls):
            return Field("Country")

        @classmethod
        def description(cls):
            return Field("Description")

        @classmethod
        def record_image(cls):
            return Field("Record_Image")

        @classmethod
        def last_visited_time(cls):
            return Field("Last_Visited_Time")

        @classmethod
        def first_visited_time(cls):
            return Field("First_Visited_Time")

        @classmethod
        def referrer(cls):
            return Field("Referrer")

        @classmethod
        def first_visited_url(cls):
            return Field("First_Visited_URL")

        @classmethod
        def number_of_chats(cls):
            return Field("Number_Of_Chats")

        @classmethod
        def average_time_spent_minutes(cls):
            return Field("Average_Time_Spent_Minutes")

        @classmethod
        def days_visited(cls):
            return Field("Days_Visited")

        @classmethod
        def visitor_score(cls):
            return Field("Visitor_Score")

    class Deals:
        @classmethod
        def owner(cls):
            return Field("Owner")

        @classmethod
        def amount(cls):
            return Field("Amount")

        @classmethod
        def deal_name(cls):
            return Field("Deal_Name")

        @classmethod
        def closing_date(cls):
            return Field("Closing_Date")

        @classmethod
        def account_name(cls):
            return Field("Account_Name")

        @classmethod
        def stage(cls):
            return Field("Stage")

        @classmethod
        def probability(cls):
            return Field("Probability")

        @classmethod
        def expected_revenue(cls):
            return Field("Expected_Revenue")

        @classmethod
        def type(cls):
            return Field("Type")

        @classmethod
        def currency(cls):
            return Field("Currency")

        @classmethod
        def next_step(cls):
            return Field("Next_Step")

        @classmethod
        def lead_source(cls):
            return Field("Lead_Source")

        @classmethod
        def campaign_source(cls):
            return Field("Campaign_Source")

        @classmethod
        def contact_name(cls):
            return Field("Contact_Name")

        @classmethod
        def created_by(cls):
            return Field("Created_By")

        @classmethod
        def modified_by(cls):
            return Field("Modified_By")

        @classmethod
        def created_time(cls):
            return Field("Created_Time")

        @classmethod
        def tag(cls):
            return Field("Tag")

        @classmethod
        def modified_time(cls):
            return Field("Modified_Time")

        @classmethod
        def territory(cls):
            return Field("Territory")

        @classmethod
        def exchange_rate(cls):
            return Field("Exchange_Rate")

        @classmethod
        def last_activity_time(cls):
            return Field("Last_Activity_Time")

        @classmethod
        def lead_conversion_time(cls):
            return Field("Lead_Conversion_Time")

        @classmethod
        def sales_cycle_duration(cls):
            return Field("Sales_Cycle_Duration")

        @classmethod
        def overall_sales_duration(cls):
            return Field("Overall_Sales_Duration")

        @classmethod
        def deal_category_status(cls):
            return Field("Deal_Category_Status")

        @classmethod
        def description(cls):
            return Field("Description")





