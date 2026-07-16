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
        self._history = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
        self._history.append(("deposit", amount))
        self._notify(f"{self.owner} deposited {amount:.2f} ETB")

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

    def undo_last(self):
        if not self._history:
            print("No transactions to undo.")
        action, amount = self._history.pop()
        if action == "deposit":
            self._Account__balance -= amount
        elif action == "withdraw":
            self._Account__balance += amount
        self._notify(f"{self.owner} undid the last {action} of {amount:.2f} ETB")
        print("Last transaction undone.")

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
        self._history.append(("withdraw", amount))
        self._notify(f"{self.owner} withdrew {amount:.2f} ETB")

    def statement(self):
        super().statement()
        print(
            f"[Savings] {self.owner} | "
            f"Account: {self.account_number} | "
            f"Balance: {self.balance:.2f} ETB"
        )

class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=1000):
        super().__init__(owner, number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        super().withdraw(amount)
        if amount > self.balance + self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        self._Account__balance -= amount
        self._history.append(("withdraw", amount))
        self._notify(f"{self.owner} withdrew {amount:.2f} ETB")

    def statement(self):
        super().statement()
        print(
            f"[Current] {self.owner} | "
            f"Account: {self.account_number} | "
            f"Balance: {self.balance:.2f} ETB"
        )

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
    def list_all(self):
        for number in self.order:
            self.by_number[number].statement()

class AccountRegistry:
    def __init__(self):
        self.by_number = {}
        self.order = []

    def add(self, acc):
        self.by_number[acc.account_number] = acc
        self.order.append(acc.account_number)

    def find(self, number):
        return self.by_number.get(number)
    
    def list_all(self):
        for number in self.order:
            self.by_number[number].statement()

acc1 = AccountFactory.create("savings", "Abebe", 1001, 5000)
acc2 = AccountFactory.create("current", "Selam", 1002, 2000)

sms = SMSAlert()
log = AuditLog()
acc1.subscribe(sms)
acc1.subscribe(log)

acc2.subscribe(sms)
acc2.subscribe(log)

registry = AccountRegistry()
registry.add(acc1)
registry.add(acc2)

acc1.deposit(500)
acc1.withdraw(1000)
acc1.add_interest()

acc2.deposit(1000)
acc2.withdraw(2500)

print("\nUndoing last transaction.\n")
acc1.undo_last()
acc2.undo_last()

print("\nFinding Account 1001:\n")
found = registry.find(1001)
if found:
    found.statement()

print("\nAll Accounts:\n")
registry.list_all()