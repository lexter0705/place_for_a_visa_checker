class CheckData:
    def __init__(self, jurisdiction: str, location: str,
                 visa_type: str,
                 visa_sub_type: str,
                 appointment_category: str):
        self.__jurisdiction_id = jurisdiction
        self.__location = location
        self.__visa_type = visa_type
        self.__visa_sub_type = visa_sub_type
        self.__appointment_category_id = appointment_category

    def get_data_list(self) -> list[str]:
        return [self.__jurisdiction_id, self.__location, self.__visa_type, self.__visa_sub_type,
                self.__appointment_category_id]
