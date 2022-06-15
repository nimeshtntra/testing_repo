from datetime import datetime


class TravelValidation:
    def string_validate(name):
        if not name.isalpha():
            raise Exception("A character's Name should be used. Please tell us Whats is your Name ? ")
        if len(name) < 11:
            return name
        else:
            raise ValueError("No more than 8 characters for a Name . Please tell us what your Name is ?")

    def number_validate(number):
        if not number.isdigit():
            raise Exception

        if number.isdigit():
            return number

    def date_validate(dates):
        format = "%Y-%m-%d"
        new_date = dates.replace(" ", "-").replace("/", "-").strip()
        data = datetime.strptime(new_date, format)
        if not data:
            raise Exception("Incorrect data format, should be Date Enter Date this YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD Format")
        return data