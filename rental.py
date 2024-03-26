import Pyro5.api


@Pyro5.api.expose
class rental(object):
    def __init__(self):
        self.users = []
        self.manufacturers = []
        self.rental_car = []
        self.not_rental_car = []
        self.rented_car = []

    def add_user(self, user_name, user_number):
        for repeat_name, repeat_number in self.users:
            if user_name == repeat_name:
                return False
        self.users.append((user_name, user_number))
        return True

    def return_users(self):
        if not self.users:
            return "not have users"
        else:
            index = []
            for user_name, user_number in self.users:
                index.append(f"User name: {user_name}, User number: {user_number}")
            return "\n".join(index)

    def add_manufacturer(self, manufacturer_name, manufacturer_country):
        for repeat_manufacturer_name, repeat_manufacturer_country in self.manufacturers:
            if manufacturer_name == repeat_manufacturer_name:
                return False
        self.manufacturers.append((manufacturer_name, manufacturer_country))
        return True

    def return_manufacturers(self):
        if not self.manufacturers:
            return "not have manufacturer"
        else:
            array = []
            for manufacturer_name, manufacturer_country in self.manufacturers:
                array.append(f"manufacturer name:{manufacturer_name},  manufacturer country: {manufacturer_country}")
            return "\n".join(array)

    def add_rental_car(self, manufacturer_name, car_model):
        for input_manufacturer_name, _ in self.manufacturers:
            if manufacturer_name == input_manufacturer_name:
                self.rental_car.append((manufacturer_name, car_model))
                self.not_rental_car.append((manufacturer_name, car_model))
                return True
        return False

    def return_cars_not_rented(self):
        if not self.not_rental_car:
            return "not have not rental car"
        else:
            index = []
            for manufacturer_name, car_model in self.not_rental_car:
                index.append(f"manufacturer name:{manufacturer_name}, car model:{car_model}")
            return "\n".join(index)

    def rent_car(self, user_name, car_model, year, month, day):
        for rental_manufacturer_name, rental_car_model in self.not_rental_car:
            if car_model == rental_car_model:
                if isinstance(year, int) and isinstance(month, int) and isinstance(day,
                                                                                   int) and 0 < year and 0 < month <= 12 and 0 < day <= 31:
                    self.not_rental_car.remove((rental_manufacturer_name, rental_car_model))
                    self.rented_car.append((user_name, car_model, year, month, day))
                    return "1"
        return "0"

    def return_cars_rented(self):
        if not self.rented_car:
            return "not rented car"
        else:
            index = []
        for _, car_model, _, _, _ in self.rented_car:
            for manufacturer_name, car_model_rented in self.rental_car:
                if car_model_rented == car_model:
                    index.append(
                        f"manufacturer name:{manufacturer_name}, car model:{car_model}")
                    break
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
