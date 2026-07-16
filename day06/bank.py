from abc import ABC, abstractmethod

class BankConfig:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.interest_rate = 0.05
            cls._instance.overdraft_limit = 1000
        return cls._instance

class Account(ABC):
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance
        self._observers = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount

    def subscribe(self, observer):
        self._observers.append(observer)

    def _notify(self, message):
        for observer in self._observers:
            observer.update(message)

    @abstractmethod
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    @abstractmethod
    def statement(self):
        print(f"Owner: {self.owner}")
        print(f"Account Number: {self.account_number}")

class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, rate=0.05):
        super().__init__(owner, number, balance)
        self.rate = rate

    def add_interest(self):
        self.deposit(self.balance * self.rate)

    def withdraw(self, amount):
        super().withdraw(amount)
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self._Account__balance -= amount
        self._notify(f"{self.owner} withdrew {amount:.2f} ETB")

    def statement(self):
        super().statement()
        print(f"[Savings] Balance: {self.balance:.2f} ETB")

class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=1000):
        super().__init__(owner, number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        super().withdraw(amount)
        if amount > self.balance + self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        self._Account__balance -= amount
        self._notify(f"{self.owner} withdrew {amount:.2f} ETB")

    def statement(self):
        super().statement()
        print(f"[Current] Balance: {self.balance:.2f} ETB")

class SMSAlert:
    def update(self, message):
        print(f"[SMS] {message}")

class AuditLog:
    def update(self, message):
        print(f"[LOG] {message}")

class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0):
        config = BankConfig()
        if kind.lower() == "savings":
            return SavingsAccount(owner, number, balance, config.interest_rate)
        elif kind.lower() == "current":
            return CurrentAccount(owner, number, balance, config.overdraft_limit)
        else:
            raise ValueError("Invalid account type")

acc1 = AccountFactory.create("savings", "Abebe", 1001, 5000)
acc2 = AccountFactory.create("current", "Selam", 1002, 2000)

sms = SMSAlert()
log = AuditLog()
acc1.subscribe(sms)
acc1.subscribe(log)

acc2.subscribe(sms)
acc2.subscribe(log)

acc1.deposit(500)
acc1.withdraw(1000)
acc1.add_interest()

acc2.deposit(1000)
acc2.withdraw(2500)

accounts = [acc1, acc2]
for account in accounts:
    account.statement()