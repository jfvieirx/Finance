import pytest
from datetime import datetime
from finances.classes import Client, Investment, generate_report, future_value_report


# Testando a função generate_report
def test_generate_report():
    client = Client("Ana Beatriz")
    account = client.add_account("Checking")
    account.add_transaction(1000.0, "Deposit", "Salary")
    investment = Investment("Stocks", 5000.0, 0.05)
    client.add_investment(investment)

    report = generate_report(client)

    assert "Relatório Financeiro para Ana Beatriz" in report
    assert "Checking" in report
    assert "R$ 1000.00" in report
    assert "Investimentos" in report
    assert "Ações" in report
    assert "R$ 5000.00" in report
    assert "Patrimônio Total" in report


# Testando a função future_value_report
def test_future_value_report():
    client = Client("Ana Beatriz")
    investment = Investment("Stocks", 5000.0, 0.05)
    client.add_investment(investment)

    future_date = datetime(2025, 12, 31)
    report = future_value_report(client, future_date)

    assert "Projeção de Investimentos para 31/12/2025" in report
    assert "Ações" in report
    assert "R$" in report
