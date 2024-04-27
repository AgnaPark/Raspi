class RoLicensePlate:
    COUNTY_CODES = [
        "AB", "AG", "AR", "B", "BC", "BH", "BN", "BR", "BT", "BV", "BZ", "CJ",
        "CL", "CS", "CT", "CV", "DB", "DJ", "GJ", "GL", "GR", "HD", "HR", "IF",
        "IL", "IS", "MH", "MM", "MS", "NT", "OT", "PH", "SB", "SJ", "SM", "SV",
        "TL", "TM", "TR", "VL", "VN", "VS"
    ]

    COUNTRY_CODES = [
        "101", "102", "103", "104", "105", "106", "107", "108", "109", "110",
        "111", "112", "113", "114", "115", "116", "122", "123", "124", "125",
        "126", "127", "128", "130", "131", "134", "136", "138", "141", "142",
        "146", "150", "152", "154", "155", "156", "157", "159", "165", "166",
        "167", "168", "170", "183", "189", "191", "193", "205", "206", "207",
        "210", "211", "214", "216", "217", "220", "222", "223", "226", "234"
    ]

    TEXT_CODE = ["MAI", "CD", "TC","CO", "A"]

    def __init__(self, license_str: str):
        self.state = "COUNTY"
        self.license_str = license_str.replace(" ", "")
        self.county = ""
        self.numbers = ""
        self.letters = ""

    def transition(self):
        for i in self.license_str:
            if self.state == "COUNTY":
                if i.isalpha():
                    self.county += i
                elif i.isdigit():
                    self.state = "NUMBERS"
                    self.numbers += i
            elif self.state == "NUMBERS":
                if i.isdigit():
                    self.numbers += i
                elif i.isalpha():
                    self.state = "LETTERS"
                    self.letters += i
            elif self.state == "LETTERS":
                if i.isalpha():
                    self.letters += i

    def is_valid_county_code(self):
        return self.county in self.COUNTY_CODES

    def is_valid_number_length(self):
        if self.is_valid_county_code():
            if self.county == "B":
                return 2 <= len(self.numbers) <= 3
            else:
                return len(self.numbers) == 2

    def is_valid_letters(self):
        return (self.letters[0] not in ['I', 'O'] and 'Q' not in self.letters and self.letters not in ['III', 'OOO'])

    def is_valid_country_code(self):
        return self.county in self.COUNTRY_CODES

    def is_temporary_short(self):
        numbers_str = str(self.numbers)
        return self.county in self.COUNTY_CODES and 3<= len(numbers_str) <= 6 and numbers_str[0] == '0' and numbers_str[1] != '0' and len(self.letters) == 0

    def is_temporary_long(self):
        numbers_str = str(self.numbers)
        return self.county in self.COUNTY_CODES and 3<= len(numbers_str) <= 6 and numbers_str[0] != '0' and len(self.letters) == 0

    def is_diplomatic(self):
        numbers_str = str(self.numbers)
        first_three_digits = numbers_str[:3]
        return self.county in self.TEXT_CODE and len(numbers_str) == 6 and first_three_digits in self.COUNTRY_CODES

    def is_valid(self):
        return self.is_valid_county_code() and self.is_valid_number_length() and self.is_valid_letters()
    
    def is_roLicensePlate(self):
        
        self.transition()
                
        if(self.is_valid()):
            return True
        elif(self.is_diplomatic()):
            return True
        elif(self.is_temporary_short()):
            return True
        elif(self.is_temporary_long()):
            return True
        else:
            return False

    def __repr__(self):
        return f"<RoLicensePlateStateMachine county = {self.county}, numbers = {self.numbers}, letters = {self.letters}>"
