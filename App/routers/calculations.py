def add(a:int, b:int):
    return a + b
    
def subtract(a:int, b:int):
    return a - b 

def multiply(a:int, b:int):
    
    return a * b

def divide(a:int, b:int):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount): 
        if amount > self.balance:
            raise Exception("Insufficient funds")
        self.balance -= amount

    def collect_interest(self, rate):    
        self.balance += self.balance * rate

class InsufficientFunds(Exception):
    pass