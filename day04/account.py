class Account:
    def __init__(self, owner, number, balance=0):
        self.owner=owner
        self.account_number=number
        self.__balance=balance
    @property
    def balance(self):
        return self.__balance
    def deposit(self, amount):
        if amount<=0:
            raise ValueError("Must be positive")
        self.__balance+=amount
    def withdraw(self, amount):
        if amount<=0:
            raise ValueError("Must be positive")
        if amount>self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance-=amount
    def statement(self):
        print("Owner:", self.owner)
        print("Account Number:", self.account_number)
        print("Balance:", self.balance, "ETB")

acc1 = Account("Yordanos", 1001, 2000)
acc2 = Account("Abebe", 1002, 3000)
acc1.deposit(1000)
acc2.withdraw(500)
acc1.statement()
print()
acc2.statement()