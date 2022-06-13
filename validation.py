from datetime import datetime


class TravelValidation:
    def string_validate(name):
        if not name.isalpha():
            raise Exception
        if len(name) < 11:
            return name
        else:
            raise ValueError

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
            raise Exception
        if data:
            return data