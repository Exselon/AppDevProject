class User:
    def __init__(self, first_name, last_name, user_email, gender, user_type):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__user_email = user_email
        self.__gender = gender
        self.__user_type = "customer"

        def get_first_name(self):
            return self.__firstname

        def get_last_name(self):
            return self.__last_name

        def get_user_email(self):
            return self.__user_email

        def get_user_type(self):
            return self.__user_type

        # -------------Set-------------

        def set_first_name(self, first_name):
             self.__firstname = first_name

        def set_last_name(self, last_name):
            self.__last_name = last_name

        def set_user_email(self, user_email):
            return self.__user_email

        def set_user_type(self, user_type):
            self.__user_type = "customers"