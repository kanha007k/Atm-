import time

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.account_balance = 0
        self.transaction_history = []

    def authenticate(self, entered_pin):
        return self.pin == entered_pin

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)

    def check_balance(self):
        return self.account_balance

    def transfer(self, recipient, amount):
        if amount > 0 and amount <= self.account_balance:
            self.account_balance -= amount
            recipient.account_balance += amount
            self.add_transaction(f"Transferred RS{amount} to {recipient.user_id}")
            recipient.add_transaction(f"Received RS{amount} from {self.user_id}")
            return True
        return False

class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def print_welcome(self):
        print("*" * 50)
        print(" " * 10 + "Welcome to the ATM INTERFACE")
        print("*" * 50)
        print(" " * 2 + "We're excited to assist you with our services.")
        time.sleep(1)
        print(" " * 6 + "Please proceed to the options below.")
        time.sleep(1)
        print("*" * 50)

    def create_user(self, user_id, pin):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, pin)
            print("Account created successfully. Thank you for choosing our ATM.")
        else:
            print("User ID already exists. Please choose a different one.")

    def authenticate_user(self, user_id, pin):
        if user_id in self.users:
            user = self.users[user_id]
            if user.authenticate(pin):
                self.current_user = user
                return True
        return False

    def display_main_menu(self):
        while True:
            if self.current_user:
                print("\nMain Menu:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Check Balance")
                print("5. Transactions History")
                print("6. Logout")

                choice = input("Enter your choice (1-6): ")
                if choice == '1':
                    self.deposit()
                elif choice == '2':
                    self.withdraw()
                    print("Take your cash.")
                elif choice == '3':
                    self.transfer()
                elif choice == '4':
                    self.check_balance()
                elif choice == '5':
                    self.display_transaction_history()
                    print("Thank you for checking your transaction history with our ATM.")
                elif choice == '6':
                    print("Thanks for using the ATM. You have been logged out.")
                    self.current_user = None
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
            else:
                print("Authentication is required to access the ATM functionalities.")
                break

    def display_transaction_history(self):
        if self.current_user:
            print("\nTransaction History:")
            for transaction in self.current_user.transaction_history:
                print(transaction)
        else:
            print("Authentication is required to access the transaction history.")
        print("Thank you for using our ATM service.")

    def check_balance(self):
        if self.current_user:
            balance = self.current_user.check_balance()
            print(f"Your current balance is RS{balance}")
        else:
            print("Authentication is required to check the balance.")
        print("Thank you for using our ATM service.")

    def withdraw(self):
        if self.current_user:
            amount = float(input("Enter the withdrawal amount:₹ "))
            if amount > 0 and amount <= self.current_user.account_balance:
                self.current_user.account_balance -= amount
                self.current_user.add_transaction(f"Withdrew RS{amount}")
                print(f"Withdrew RS{amount} successfully.")
            else:
                print("Invalid amount or insufficient balance.")
        else:
            print("Authentication is required to perform a withdrawal.")
        print("Thank you for using our ATM service.")

    def deposit(self):
        if self.current_user:
            amount = float(input("Enter the deposit amount:₹ "))
            if amount > 0:
                self.current_user.account_balance += amount
                self.current_user.add_transaction(f"Deposited RS{amount}")
                print(f"Deposited RS{amount} successfully. Thank you for your deposit.")
            else:
                print("Invalid amount.")
        else:
            print("Authentication is required to make a deposit.")
        print("Thank you for using our ATM service.")

    def transfer(self):
        if self.current_user:
            recipient_id = input("Enter the recipient's User ID: ")
            if recipient_id in self.users:
                recipient = self.users[recipient_id]
                amount = float(input(f"Enter the transfer amount to {recipient_id}:₹ "))
                if self.current_user.transfer(recipient, amount):
                    print(f"Transferred RS{amount} to {recipient_id} successfully.")
                else:
                    print("Invalid amount or insufficient balance.")
            else:
                print("Recipient User ID not found.")
        else:
            print("Authentication is required to perform a transfer.")
        print("Thank you for using our ATM service.")

    def login_menu(self):
        self.print_welcome()
        while True:
            print("1. Create User")
            print("2. Login")
            print("3. Quit")

            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                user_id = input("Enter a new User ID: ")
                pin = input("Create a PIN: ")
                self.create_user(user_id, pin)
            elif choice == '2':
                user_id = input("Enter your User ID: ")
                pin = input("Enter your PIN: ")
                if self.authenticate_user(user_id, pin):
                    self.display_main_menu()
                else:
                    print("Authentication failed. Please try again.")
            elif choice == '3':
                print("Thank you for using our ATM service.")
                return False
            else:
                print("Invalid choice. Please enter a valid option.")
            self.print_welcome()
        return True

# Create an instance of the ATM
atm = ATM()

# Run the ATM application
running = True
while running:
    running = atm.login_menu()
