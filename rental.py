import Pyro5.api
from datetime import datetime


@Pyro5.api.expose
class rental(object):
    def __init__(self):
        self.users = []
        self.manufacturers = []
        self.rental_car = []
        self.not_rental_car = []
        self.rented_car = []
        self.rented_car_recording = []
        self.end_rented_car_recording = []

    # Task 1
    def add_user(self, user_name, user_number):
        for repeat_name, repeat_number in self.users:
            if user_name == repeat_name:
                return False
        self.users.append((user_name, user_number))
        return True

    # Task 2
    def return_users(self):
        if not self.users:
            return "not have users"
        else:
            index = []
            for user_name, user_number in self.users:
                index.append(f"User name: {user_name}, User number: {user_number}")
            return "\n".join(index)

    # Task 3
    def add_manufacturer(self, manufacturer_name, manufacturer_country):
        for repeat_manufacturer_name, repeat_manufacturer_country in self.manufacturers:
            if manufacturer_name == repeat_manufacturer_name:
                return False
        self.manufacturers.append((manufacturer_name, manufacturer_country))
        return True

    # Task 4
    def return_manufacturers(self):
        if not self.manufacturers:
            return "not have manufacturer"
        else:
            array = []
            for manufacturer_name, manufacturer_country in self.manufacturers:
                array.append(f"manufacturer name:{manufacturer_name},  manufacturer country: {manufacturer_country}")
            return "\n".join(array)

    # Task 5
    def add_rental_car(self, manufacturer_name, car_model):
        for input_manufacturer_name, _ in self.manufacturers:
            if manufacturer_name == input_manufacturer_name:
                self.rental_car.append((manufacturer_name, car_model))
                self.not_rental_car.append((manufacturer_name, car_model))
                return True
        return False

    # Task 6
    def return_cars_not_rented(self):
        if not self.not_rental_car:
            return "not have not rental car"
        else:
            index = []
            for manufacturer_name, car_model in self.not_rental_car:
                index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
            return "\n".join(index)

    # Task 7
    def rent_car(self, user_name, car_model, year, month, day):
        if isinstance(year, int) and isinstance(month, int) and isinstance(day,
                                                                           int) and 0 < year and 0 < month <= 12 and 0 < day <= 31:
            rent_time = datetime(year, month, day)
            for rental_manufacturer_name, rental_car_model in self.not_rental_car:
                if car_model == rental_car_model:
                    self.not_rental_car.remove((rental_manufacturer_name, rental_car_model))
                    self.rented_car_recording.append((user_name, car_model, rent_time))
                    self.rented_car.append((rental_manufacturer_name, rental_car_model))
                    return "1"
        else:
            return "0"

    # Task8
    def return_cars_rented(self):
        if not self.rented_car:
            return "not rented car"
        else:
            index = []
        for manufacturer_name, car_model in self.rented_car:
            index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
        return "\n".join(index)

    # Task 9
    def end_rental(self, user_name, car_model, year, month, day):
        if isinstance(year, int) and isinstance(month, int) and isinstance(day,
                                                                           int) and 0 < year and 0 < month <= 12 and 0 < day <= 31:
            end_time = datetime(year, month, day)
            for manufacturer_name, rented_car_model in self.rented_car:
                if car_model == rented_car_model:
                    self.rented_car.remove((manufacturer_name, rented_car_model))
                    self.not_rental_car.append((manufacturer_name, rented_car_model))
            for rented_user_name, rented_car_model, rented_date in self.rented_car_recording:
                if user_name == rented_user_name and car_model == rented_car_model:
                    self.end_rented_car_recording.append((rented_user_name, rented_car_model, rented_date, end_time))
                    self.rented_car_recording.remove((rented_user_name, rented_car_model, rented_date))

    # Task 12
    def user_rental_date(self, user_name, start_year, start_month, start_day, end_year,
                         end_month, end_day):
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)
        index = []
        for recording_user, recording_model, rental_time, back_time in self.end_rented_car_recording:
            if recording_user == user_name and rental_time > start_date and back_time < end_date:
                for factor_name, car_model in self.rental_car:
                    if recording_model == car_model:
                        index.append(f"manufacturer name:{factor_name}, car model:{car_model}")
                return "\n".join(index)


def main():
    demo = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    rental_obj = rental()
    url = demo.register(rental_obj)
    ns.register("example.rental", url)
    print(url)
    demo.requestLoop()


if __name__ == "__main__":
    main()
