import Pyro5.api


@Pyro5.api.expose
class rental(object):
    def __init__(self):
        self.users = []

    def add_user(self, user_name, user_number):
        self.users.append((user_name, user_number))
        return True


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
