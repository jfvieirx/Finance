import pytest
from datetime import datetime
from finances.classes import Transaction, Account, Investment, Client


# Testando a classe Transaction
def test_transaction_creation():
    transaction = Transaction(100.0, "Food", "Lunch")
    assert transaction.amount == 100.0
    assert transaction.category == "Food"
    assert transaction.description == "Lunch"
    assert isinstance(transaction.date, datetime)


def test_transaction_update():
    transaction = Transaction(100.0, "Food", "Lunch")
    transaction.update(amount=150.0, description="Dinner")
    assert transaction.amount == 150.0
    assert transaction.description == "Dinner"


# Testando a classe Account
def test_account_creation():
    account = Account("Checking")
    assert account.name == "Checking"
    assert account.balance == 0.0
    assert len(account.transactions) == 0


def test_account_add_transaction():
    account = Account("Checking")
    transaction = account.add_transaction(1000.0, "Deposit", "Salary")
    assert account.balance == 1000.0
    assert len(account.transactions) == 1
    assert transaction.amount == 1000.0
    assert transaction.category == "Deposit"


# Testando a classe Investment
def test_investment_creation():
    investment = Investment("Stocks", 1000.0, 0.05)
    assert investment.type == "Stocks"
    assert investment.initial_amount == 1000.0
    assert investment.rate_of_return == 0.05
    assert isinstance(investment.date_purchased, datetime)


def test_investment_calculate_value():
    investment = Investment("Stocks", 1000.0, 0.05)
    value = investment.calculate_value()
    assert value > 1000.0


# Testando a classe Client
def test_client_creation():
    client = Client("John Doe")
    assert client.name == "John Doe"
    assert len(client.accounts) == 0
    assert len(client.investments) == 0


def test_client_add_account():
    client = Client("John Doe")
    account = client.add_account("Savings")
    assert len(client.accounts) == 1
    assert account.name == "Savings"


def test_client_add_investment():
    client = Client("John Doe")
    investment = Investment("Stocks", 5000.0, 0.05)
    client.add_investment(investment)
    assert len(client.investments) == 1
    assert client.investments[0] == investment
