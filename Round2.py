import datetime

class Theatre:

    def __init__(self, name, popcorn_price, sandwich_price, location) -> None:
        self.name = name
        self.screens = [Gold(), iMax(), General()]
        self.location = location
        self.food_prices = {"popcorn": popcorn_price, "sandwich": sandwich_price}


    def __str__(self) -> str:
        return self.name + " at " + self.location

    def __repr__(self) -> str:
        return self.name + " at " + self.location

    def get_screens(self):
        return self.screens

    def get_food_price(self, ticket, food):
        return self.food_prices[food] - self.food_prices[food] * ticket.get_discount()

    def book_ticket(self, screen_index, user):
        self.screens[screen_index].book_ticket(user)

    def get_bookings(self):
        for screen in self.screens:
            print(screen, screen.get_bookings())

class Screen:

    def __init__(self, name, ticket_price, food_discount, screen_size, time) -> None:
        self.ticket_price = ticket_price
        self.food_discount = food_discount
        self.name = name
        self.screen_size = screen_size
        self.time = time

        self.sold_to = []

    def __str__(self) -> str:
        return f"{self.name} at ${self.ticket_price} with food_discount: {self.food_discount}%"
    
    def get_bookings(self):
        return self.sold_to

    def get_price(self):
        return self.ticket_price

    def get_discount(self):
        return self.food_discount / 100

    def sold_out(self):
        return len(self.sold_to) >= self.screen_size

    def book_ticket(self, user):
        self.sold_to.append(user)
    
    def remove_booking(self, user):
        self.sold_to.remove(user)

class Gold(Screen):

    def __init__(self) -> None:
        time_delta = datetime.timedelta(minutes=10)
        super().__init__("Gold", 400, 10, 2, datetime.datetime.now() + time_delta)

class iMax(Screen):

    def __init__(self) -> None:
        time_delta = datetime.timedelta(minutes=20)
        super().__init__("iMax", 300, 5, 5, datetime.datetime.now() + time_delta)

class General(Screen):

    def __init__(self) -> None:
        time_delta = datetime.timedelta(minutes=40)
        super().__init__("General", 200, 0, 10, datetime.datetime.now() + time_delta)



class User:

    def __init__(self, balance) -> None:
        self.balance = balance
        self.tickets = []
        self.basket = []

    def get_balance(self):
        return self.balance

    def buy_ticket(self, ticket):
        if(self.balance >= ticket.get_price()):
            self.balance-=ticket.get_price()
            self.tickets.append(ticket)
            return True
        return False

    def get_bookings(self):
        return self.tickets

    def buy_food(self, food, screen, theatre):
        
        price = theatre.get_food_price(screen, food)

        if(self.balance >= price):
            self.balance-= price
            return True
        return False

    def add_food(self, food):
        self.basket.append(food)


    def __repr__(self) -> str:
        return f"User, Balance: {self.get_balance()}"

    def __str__(self) -> str:
        return f"User, Balance: {self.get_balance()}"


def main():
    theatres = []

    with open("theatres.txt", "r") as f:
        file_read = f.readlines()
        for i in file_read:
            data = i.split()
            theatres.append(Theatre(data[0], int(data[1]), int(data[2]), data[3]))

    bal = int(input("Enter your wallet balance:"))
    user = User(bal)

    while True:
        print("""
            Choose a action:
                1.Book a Movie Ticket.
                2.Get Bookings
                3.Cancel Booking
            """)

        Input = int(input())

        if(Input == 1):
            print("Available Theatres")

            for i in range(len(theatres)):
                print(f"{i+1}. {theatres[i]}")

            theatre_selected = int(input("Select a theatre:")) - 1


            print("Screens:")

            screens = theatres[theatre_selected].get_screens()
            for i in range(len(screens)):
                print(f"{i+1}. {screens[i]}")

            screen_selected = int(input("Select a Screen:")) - 1

            transaction = user.buy_ticket(screens[screen_selected])

            if transaction:
                print("Bought ticket successfully, Wallet Balance:" + f"${user.get_balance()}")
                theatres[theatre_selected].book_ticket(screen_selected, user)
            else:
                print("Not enough money in wallet!")

            print("Food and Beverages Section:")

            available_foods = theatres[theatre_selected].food_prices

            foods_selected = []

            while True:

                for foods in available_foods.keys():
                    print(f"{foods} at ${theatres[theatre_selected].get_food_price(screens[screen_selected], foods)}")
                print("Skip")

                option = input("Enter name of the food to purchase or skip to continue:").lower()

                if option == "skip":
                    break

                food_transaction = user.buy_food(option,screens[screen_selected],  theatres[theatre_selected])


                if food_transaction:
                    print(f"Bought {option.capitalize()} sucessfully, Wallet Balance: {user.get_balance()}")
                    user.add_food(option)
                else:
                    print("Not enough money")

        if(Input == 2):
            while True:
                print("Available Theatres")

                for i in range(len(theatres)):
                    print(f"{i+1}. {theatres[i]}")
                print(f"{i+2}. Exit")

                theatre_selected = int(input("Select a theatre:")) - 1

                if(theatre_selected == i+1):
                    break

                theatres[theatre_selected].get_bookings()

        if(Input == 3):
            print("Booked tickets:")
            booekd = user.get_bookings()
            for i in range(len(booekd)):
                print(i+1, booekd[i])

            inp = int(input("enter ticket to cancel:")) - 1
            time_diff = datetime.timedelta(minutes=30)

            if(booekd[inp].time > datetime.datetime.now() + time_diff ):
                booekd[inp].remove_booking(user)
                print("Cancelled Booking")
            else:
                print("Can't cancel bookings")

main()