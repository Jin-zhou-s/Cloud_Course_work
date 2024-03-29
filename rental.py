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
                return print("Already have a user of the same name")
        self.users.append((user_name, user_number))
        return print("Add successfully")

    # Task 2
    def return_users(self):
        if not self.users:
            return "not have users"
        else:
            index = []
            for user_name, user_number in self.users:
                index.append(f"User name: {user_name}, Phone number: {user_number}")
            return "User data:\n" + "\n".join(index)

    # Task 3
    def add_manufacturer(self, manufacturer_name, manufacturer_country):
        for repeat_manufacturer_name, repeat_manufacturer_country in self.manufacturers:
            if manufacturer_name == repeat_manufacturer_name:
                return print("There is already a manufacturer of the same name")
        self.manufacturers.append((manufacturer_name, manufacturer_country))
        return print("Add successfully")

    # Task 4
    def return_manufacturers(self):
        if not self.manufacturers:
            return "not have manufacturer"
        else:
            array = []
            for manufacturer_name, manufacturer_country in self.manufacturers:
                array.append(f"manufacturer name:{manufacturer_name},  manufacturer country: {manufacturer_country}")
            return "manufacturer data:\n" + "\n".join(array)

    # Task 5
    def add_rental_car(self, manufacturer_name, car_model):
        for input_manufacturer_name, input_car_model in self.rental_car:
            if manufacturer_name != input_manufacturer_name and car_model == input_car_model:
                return print("Vehicle model does not match manufacturer")
        for input_manufacturer_name, _ in self.manufacturers:
            if manufacturer_name == input_manufacturer_name:
                self.rental_car.append((manufacturer_name, car_model))
                self.not_rental_car.append((manufacturer_name, car_model))
                return print("Add successfully")
        return print("not available from this manufacturer")

    # Task 6
    def return_cars_not_rented(self):
        if not self.not_rental_car:
            return "not have not rental car"
        else:
            index = []
            for manufacturer_name, car_model in self.not_rental_car:
                index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
            return "not rented car:\n" + "\n".join(index)

    # Task 7
    def rent_car(self, user_name, car_model, year, month, day):
        found = False
        for name, _ in self.users:
            if user_name == name:
                found = True
                break
        if not found:
            return print("not have this user")
        for name, car, _ in self.rented_car_recording:
            if user_name == name and car_model == car:
                return print("cant to rent same model car ")
        try:
            rent_time = datetime(year, month, day)
        except ValueError as e:
            return print("Incorrect date")
        except TypeError as e:
            return print("The date cannot be a floating point number")
        except OverflowError as e:
            return print("Exceeding the date length limit, the date year should be 1 to 9999 years")
        for rental_manufacturer_name, rental_car_model in self.not_rental_car:
            if car_model == rental_car_model:
                self.not_rental_car.remove((rental_manufacturer_name, rental_car_model))
                self.rented_car_recording.append((user_name, car_model, rent_time))
                self.rented_car.append((rental_manufacturer_name, rental_car_model))
                return 1
        else:
            return 0

    # Task8
    def return_cars_rented(self):
        if not self.rented_car:
            return "not rented car"
        else:
            index = []
        for manufacturer_name, car_model in self.rented_car:
            index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
        return "rented car:\n" + "\n".join(index)

    # Task 9
    def end_rental(self, user_name, car_model, year, month, day):
        found = False
        for name, car, _ in self.rented_car_recording:
            if user_name == name and car_model == car:
                found = True
        if not found:
            return print("user have rented this model car")
        try:
            end_date = datetime(year, month, day)
        except ValueError as e:
            return print("Incorrect date")
        except TypeError as e:
            return print("The date cannot be a floating point number")
        except OverflowError as e:
            return print("Exceeding the date length limit, the date year should be 1 to 9999 years")
        for rented_user_name, rented_car_model, rented_date in self.rented_car_recording:
            if user_name == rented_user_name and car_model == rented_car_model and rented_date <= end_date:
                self.end_rented_car_recording.append((rented_user_name, rented_car_model, rented_date, end_date))
                self.rented_car_recording.remove((rented_user_name, rented_car_model, rented_date))
            else:
                return print("The return date must be after the borrowing date (can be the same day)")
        for manufacturer_name, rented_car_model in self.rented_car:
            if car_model == rented_car_model:
                self.rented_car.remove((manufacturer_name, rented_car_model))
                self.not_rental_car.append((manufacturer_name, rented_car_model))
                return print("Successful restitution")

    # Task 10
    def delete_car(self, car_model):
        self.not_rental_car = list(filter(lambda x: x[1] != car_model, self.not_rental_car))
        return print("car delete finish")

    # Task 11
    def delete_user(self, user_name):
        for ed_delete_user, _, _ in self.rented_car_recording:
            if user_name == ed_delete_user:
                return print("can't delete this user")
        for end_delete_user, _, _, _ in self.end_rented_car_recording:
            if user_name == end_delete_user:
                return print("can't delete this user")
        self.users = list(filter(lambda x: x[0] != user_name, self.users))
        return print("delete finish")

    # Task 12
    def user_rental_date(self, user_name, start_year, start_month, start_day, end_year,
                         end_month, end_day):
        try:
            start_date = datetime(start_year, start_month, start_day)
            end_date = datetime(end_year, end_month, end_day)
        except ValueError as e:
            return "Incorrect date"
        except TypeError as e:
            return "The date cannot be a floating point number"
        except OverflowError as e:
            return "Exceeding the date length limit, the date year should be 1 to 9999 years"
        index = []
        for recording_user, recording_model, rental_time, back_time in self.end_rented_car_recording:
            if recording_user == user_name and rental_time >= start_date and back_time <= end_date:
                for factor_name, car_model in self.rental_car:
                    if recording_model == car_model:
                        index.append(f"manufacturer name:{factor_name}, car model:{car_model}")
                        break
        return "User rental history:\n" + "\n".join(index)


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
