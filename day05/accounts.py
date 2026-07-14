from abc import ABC, abstractmethod

class Account(ABC):
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
    @abstractmethod
    def withdraw(self, amount):
        pass
    @abstractmethod
    def statement(self):
        pass

class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, rate=0.05):
        super().__init__(owner, number, balance)
        self.rate=rate
    def add_interest(self):
        self.deposit(self.balance * self.rate)
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self._Account__balance -= amount
    def statement(self):
        print(f"[Savings] {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")

class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=1000):
        super().__init__(owner, number, balance)
        self.overdraft=overdraft
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance + self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        self._Account__balance -= amount
    def statement(self):
        print(f"[Current] {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")

acc1=SavingsAccount("Abebe", 1001, 5000)
acc2=CurrentAccount("Selam", 1002, 2000)

acc1.deposit(500)
acc1.withdraw(1000)
acc1.add_interest()

acc2.deposit(1000)
acc2.withdraw(2500)

accounts=[acc1, acc2]
for account in accounts:
    account.statement()