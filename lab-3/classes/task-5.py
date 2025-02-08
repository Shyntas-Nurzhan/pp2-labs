class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}tg. New balance: {self.balance}tg")
        else:
            print("Deposit amount must be positive!")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds! Withdrawal denied.")
        elif amount > 0:
            self.balance -= amount
            print(f"Withdrew {amount}tg. New balance: {self.balance}tg")
        else:
            print("Withdrawal amount must be positive!")
    
    def show_balance(self):
        print(f"{self.owner}'s Account Balance: {self.balance}tg")

Beka_account = Account("Beka", 250)

Beka_account.show_balance()

Beka_account.deposit(50)
Beka_account.deposit(100)

Beka_account.show_balance()

Beka_account.withdraw(300)
Beka_account.withdraw(500)

Beka_account.show_balance()