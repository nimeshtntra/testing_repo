from datetime import datetime
import re


class TravelValidation:
    def name_validate(name):
        if not name.isalpha():
            raise Exception("A character's Name should be used. Please tell us Whats is your Name ? ")
        if len(name) > 8:
            raise ValueError("No more than 8 characters for a Name . Please tell us what your Name is ?")
        return name

    def number_validate(number):
        pattern = re.compile("(0|91)?[6-9][0-9]{9}")
        if not number.isdigit():
            raise Exception("A Moble Number should be just that: a Number. Please tell us What is your Mobile Number ?")
        if not pattern.match(number):
            raise ValueError("This Mobile Number is Not Correct. Please tell us What is your Mobile Number ?  ")
        if len(number) != 10:
            raise TypeError("The Mobile Number should only be 10 digit only.Please tell us What is your Mobile Number ? ")
        return number

    def origin_validate(origin):
        if not origin.isalpha():
            raise Exception("Origin should be a character. Please tell us What is Origin ? ")
        if len(origin) > 10:
            raise ValueError("Origin Character no more than 10 .Please tell us What is Origin ?")
        return origin

    def destination_validate(destination):
        if not destination.isalpha():
            raise Exception("Destination should be a character. Please tell us your  Destination name? ")
        if len(destination) > 10:
            raise ValueError("Destination Character no more than 10 .Please tell us your  Destination name ? ")
        return destination

    def date_validate(dates):
        try:
            format = "%Y-%m-%d"
            new_date = dates.replace(" ", "-").replace("/", "-").strip()
            data = datetime.strptime(new_date, format)
            today_date = datetime.datetime.today().date()
            print('new_date',new_date)
            print('data',data)
            # if data:
            #     print('if',data)
            #     return data
            if data.date() >= today_date:
                raise TypeError("Past Date is not valid. Enter Correct Date")
            return data
        except Exception:
            raise ValueError("Incorrect data format, should be Date Enter Date this YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD Format")

    def passenger_validate(passenger):
        if not passenger.isdigit():
            raise Exception("Passenger Capacity should be a number. Enter How Many Passenger Capacity ?")
        if int(passenger) > 51:
            raise ValueError("Passenger Capacity no more than 51 .Please Enter How Many Passenger Capacity ? ")
        return passenger