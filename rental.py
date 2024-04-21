from Pyro5.api import expose, Daemon, serve
from datetime import datetime


@expose
class rental(object):
    def __init__(self):
        # user information(users name, phone number)
        self.users = []
        # Manufacturer Information(manufacturer name, country)
        self.manufacturers = []
        # List of rented vehicles(manufacturer name,car model)
        self.rental_car = []
        # Cars not rented out(manufacturer name,car model)
        self.not_rental_car = []
        # Rented out car(manufacturer name,car model)
        self.rented_car = []
        # Borrowed Vehicle Records(users name, car model, borrow date)
        self.rented_car_recording = []
        # Completed car rental records
        self.end_rented_car_recording = []

    # Task 1 - Add User
    def add_user(self, user_name, user_number):
        for repeat_name, repeat_number in self.users:
            # If names are duplicated
            if user_name == repeat_name:
                return print("Already have a user of the same name")
        # Add Data
        self.users.append((str(user_name), str(user_number)))
        return print("Add successfully")

    # Task 2 - Return user information
    def return_users(self):
        # If the user is null
        if not self.users:
            return "not have users"
        else:
            index = []
            for user_name, user_number in self.users:
                index.append(f"User name: {user_name}, Phone number: {user_number}")
            return "User data:\n" + "\n".join(index)

    # Task 3 - Add Manufacturer
    def add_manufacturer(self, manufacturer_name, manufacturer_country):
        for repeat_manufacturer_name, repeat_manufacturer_country in self.manufacturers:
            # If a manufacturer with the same name already exists
            if manufacturer_name == repeat_manufacturer_name:
                return print("There is already a manufacturer of the same name")
        self.manufacturers.append((str(manufacturer_name), str(manufacturer_country)))
        return print("Add successfully")

    # Task 4 - Back to Manufacturer Information
    def return_manufacturers(self):
        # If the manufacturer is empty
        if not self.manufacturers:
            return "not have manufacturer"
        else:
            array = []
            for manufacturer_name, manufacturer_country in self.manufacturers:
                array.append(f"manufacturer name:{manufacturer_name},  manufacturer country: {manufacturer_country}")
            return "manufacturer data:\n" + "\n".join(array)

    # Task 5 - Adding a car for rent
    def add_rental_car(self, manufacturer_name, car_model):
        for input_manufacturer_name, input_car_model in self.rental_car:
            # If the same car model already exists with a different manufacturer's name
            if manufacturer_name != input_manufacturer_name and car_model == input_car_model:
                return print("Vehicle model does not match manufacturer")
        for input_manufacturer_name, _ in self.manufacturers:
            # If the manufacturer has added
            if manufacturer_name == input_manufacturer_name:
                self.rental_car.append((str(manufacturer_name), str(car_model)))
                self.not_rental_car.append((str(manufacturer_name), str(car_model)))
                return print("Add successfully")
        return print("not available from this manufacturer")

    # Task 6 - Return of cars that were not rented
    def return_cars_not_rented(self):
        # If there are no cars that have not yet been hired
        if not self.not_rental_car:
            return "not have not rental car"
        else:
            index = []
            for manufacturer_name, car_model in self.not_rental_car:
                index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
            return "not rented car:\n" + "\n".join(index)

    # Task 7 - Rental of cars by users
    def rent_car(self, user_name, car_model, year, month, day):
        found = False
        for name, _ in self.users:
            # If there is this user
            if user_name == name:
                found = True
                break
        # Without this user
        if not found:
            return print("not have this user")
        for name, car, _ in self.rented_car_recording:
            # If the user has rented a car of the same model
            if user_name == name and car_model == car:
                return print("cant to rent same model car ")
        # date determination
        try:
            rent_time = datetime(year, month, day)
        # If the date is wrong (40 December 2020)
        except ValueError as e:
            return print("Incorrect date")
        # If the date type is incorrect (2020.12, December, 21st)
        except TypeError as e:
            return print("The date cannot be a floating point number")
        # If the date is out of limits
        except OverflowError as e:
            return print("Exceeding the date length limit, the date year should be 1 to 9999 years")
        for rental_manufacturer_name, rental_car_model in self.not_rental_car:
            # If there is a car of this model in the car that is not rented
            if car_model == rental_car_model:
                self.not_rental_car.remove((rental_manufacturer_name, rental_car_model))
                self.rented_car_recording.append((user_name, car_model, rent_time))
                self.rented_car.append((rental_manufacturer_name, rental_car_model))
                return 1
        else:
            return 0

    # Task8 - Back to Rented Car Information
    def return_cars_rented(self):
        # If the car is not rented
        if not self.rented_car:
            return "not rented car"
        else:
            index = []
        for manufacturer_name, car_model in self.rented_car:
            index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
        return "rented car:\n" + "\n".join(index)

    # Task 9 - Return of rented cars by users
    def end_rental(self, user_name, car_model, year, month, day):
        found = False
        date = False
        # If the user has a borrowed car of this model
        for name, car, _ in self.rented_car_recording:
            if user_name == name and car_model == car:
                found = True
        # If the user has not borrowed this model of car
        if not found:
            return print("user have not rented this model car")
        try:
            end_date = datetime(year, month, day)
        except ValueError as e:
            return print("Incorrect date")
        except TypeError as e:
            return print("The date cannot be a floating point number")
        except OverflowError as e:
            return print("Exceeding the date length limit, the date year should be 1 to 9999 years")

        for rented_user_name, rented_car_model, rented_date in self.rented_car_recording:
            # The date of return must be greater than or equal to the date of hire,
            # and there must be a corresponding users name and car model in the record of hired cars
            if user_name == rented_user_name and car_model == rented_car_model and rented_date <= end_date:
                self.end_rented_car_recording.append((rented_user_name, rented_car_model, rented_date, end_date))
                self.rented_car_recording.remove((rented_user_name, rented_car_model, rented_date))
                date = True
                break
            # No corresponding rental records

        if not date:
            return print("The return date must be after the borrowing date (can be the same day)")
        for manufacturer_name, rented_car_model in self.rented_car:
            # If the vehicle model is the same
            if car_model == rented_car_model:
                self.rented_car.remove((manufacturer_name, rented_car_model))
                self.not_rental_car.append((manufacturer_name, rented_car_model))
            return print("Successful restitution")

    # Task 10 - Deletion of not rented cars of specified models
    def delete_car(self, car_model):
        # Delete all cars of this model that have not been rented(x[0]: manufacturer_name, x[1]: car_model)
        self.not_rental_car = list(filter(lambda x: x[1] != car_model, self.not_rental_car))
        return print("car delete finish")

    # Task 11 - Delete users who have not rented a car
    def delete_user(self, user_name):
        for ed_delete_user, _, _ in self.rented_car_recording:
            # Is there a record of a car that was hired but not returned, if so: it cannot be deleted
            if user_name == ed_delete_user:
                return print("can't delete this user")
        for end_delete_user, _, _, _ in self.end_rented_car_recording:
            # Is there a complete record of the car hire, if so: it cannot be deleted
            if user_name == end_delete_user:
                return print("can't delete this user")
        for user, _ in self.users:
            if user_name == user:
                self.users = list(filter(lambda x: x[0] != user_name, self.users))
                return print("delete finish")
        return print("not have this user")

    # Task 12 - Returns all car hire information for a user over a period of time
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
        if end_date < start_date:
            return "The start date must be no later than the end date"
        for recording_user, recording_model, rental_time, back_time in self.end_rented_car_recording:
            # If this user exists and the recorded time is within the search range
            if recording_user == user_name and rental_time >= start_date and back_time <= end_date:
                # Search for manufacturers using the car model in the record
                for factor_name, car_model in self.rental_car:
                    if recording_model == car_model:
                        index.append(f"manufacturer name:{factor_name}, car model:{car_model}")
                        break
        if len(index) < 1:
            return "User rental history:\nnot have this user's history"
        return "User rental history:\n" + "\n".join(index)


def main():
    daemon = Daemon()
    rental_object = rental()
    serve({rental_object: "example.rental"}, daemon=daemon, use_ns=True)


if __name__ == "__main__":
    main()
