from datetime import datetime
from typing import List, Optional


class Transaction:
    """
    Classe para representar transações financeiras.

    Atributos:
        amount (float): Valor da transação.
        date (datetime): Data da transação.
        category (str): Categoria associada à transação.
        description (str): Descrição detalhada da transação.
    """

    def __init__(self, amount: float, category: str, description: str = "") -> None:
        """
        Inicializa uma nova transação.

        Args:
            amount (float): Valor da transação.
            category (str): Categoria da transação.
            description (str, opcional): Descrição da transação. Padrão é uma string vazia.
        """
        self.amount = amount
        self.date = datetime.now()
        self.category = category
        self.description = description

    def __str__(self) -> str:
        """
        Retorna uma representação textual da transação.

        Returns:
            str: Representação no formato "Transação: {description} R$ {amount:.2f} ({category})".
        """
        return f"Transação: {self.description} R$ {self.amount:.2f} ({self.category})"

    def update(self, **attributes) -> None:
        """
        Atualiza um ou mais atributos da transação.

        Args:
            **attributes: Atributos a serem atualizados.
        """
        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Account:
    """
    Classe para representar contas financeiras que armazenam transações.

    Atributos:
        name (str): Nome da conta.
        balance (float): Saldo atual da conta.
        transactions (List[Transaction]): Lista de transações associadas à conta.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa uma nova conta.

        Args:
            name (str): Nome da conta.
        """
        self.name = name
        self.balance = 0.0
        self.transactions: List[Transaction] = []

    def add_transaction(self, amount: float, category: str, description: str = "") -> Transaction:
        """
        Adiciona uma nova transação à conta e atualiza o saldo.

        Args:
            amount (float): Valor da transação.
            category (str): Categoria da transação.
            description (str, opcional): Descrição da transação. Padrão é uma string vazia.

        Returns:
            Transaction: A transação criada.
        """
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        self.balance += amount
        return transaction

    def get_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
    ) -> List[Transaction]:
        """
        Retorna uma lista de transações filtradas por data ou categoria.

        Args:
            start_date (datetime, opcional): Data inicial para o filtro.
            end_date (datetime, opcional): Data final para o filtro.
            category (str, opcional): Categoria para o filtro.

        Returns:
            List[Transaction]: Lista de transações filtradas.
        """
        filtered = self.transactions
        if start_date:
            filtered = [t for t in filtered if t.date >= start_date]
        if end_date:
            filtered = [t for t in filtered if t.date <= end_date]
        if category:
            filtered = [t for t in filtered if t.category == category]
        return filtered


class Investment:
    """
    Classe para representar investimentos financeiros.

    Atributos:
        type (str): Tipo do investimento.
        initial_amount (float): Valor inicial do investimento.
        date_purchased (datetime): Data da compra do investimento.
        rate_of_return (float): Taxa mensal de retorno.
    """

    def __init__(self, type: str, initial_amount: float, rate_of_return: float) -> None:
        """
        Inicializa um novo investimento.

        Args:
            type (str): Tipo do investimento.
            initial_amount (float): Valor inicial do investimento.
            rate_of_return (float): Taxa mensal de retorno do investimento.
        """
        self.type = type
        self.initial_amount = initial_amount
        self.date_purchased = datetime.now()
        self.rate_of_return = rate_of_return

    def calculate_value(self) -> float:
        """
        Calcula o valor atual do investimento baseado na taxa de retorno.

        Returns:
            float: Valor atual do investimento.
        """
        months_elapsed = (datetime.now().year - self.date_purchased.year) * 12 + (datetime.now().month - self.date_purchased.month)
        return self.initial_amount * ((1 + self.rate_of_return) ** months_elapsed)

    def sell(self, account: 'Account') -> None:
        """
        Vende o investimento e adiciona o valor na conta especificada.

        Args:
            account (Account): Conta onde o valor será depositado.
        """
        value = self.calculate_value()
        account.add_transaction(value, "Investment", f"Sold {self.type}")


class Client:
    """
    Classe para representar um cliente que possui contas e investimentos.

    Atributos:
        name (str): Nome do cliente.
        accounts (List[Account]): Lista de contas do cliente.
        investments (List[Investment]): Lista de investimentos do cliente.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa um novo cliente.

        Args:
            name (str): Nome do cliente.
        """
        self.name = name
        self.accounts: List[Account] = []
        self.investments: List[Investment] = []

    def add_account(self, account_name: str) -> Account:
        """
        Adiciona uma nova conta ao cliente.

        Args:
            account_name (str): Nome da conta.

        Returns:
            Account: A conta criada.
        """
        account = Account(account_name)
        self.accounts.append(account)
        return account

    def add_investment(self, investment: Investment) -> None:
        """
        Adiciona um investimento ao cliente.

        Args:
            investment (Investment): O investimento a ser adicionado.
        """
        self.investments.append(investment)

    def get_net_worth(self) -> float:
        """
        Calcula o patrimônio líquido do cliente.

        Returns:
            float: Soma dos saldos de todas as contas e o valor atual dos investimentos.
        """
        accounts_total = sum(account.balance for account in self.accounts)
        investments_total = sum(investment.calculate_value() for investment in self.investments)
        return accounts_total + investments_total


# Função de Relatório Financeiro
def generate_report(client: Client) -> str:
    """
    Gera um relatório financeiro para o cliente, incluindo contas, investimentos e patrimônio total.

    Args:
        client (Client): O cliente para quem o relatório será gerado.

    Returns:
        str: Um relatório formatado com as informações financeiras do cliente.
    """
    report = f"Relatório Financeiro para {client.name}\n"
    report += "Contas:\n"
    for account in client.accounts:
        report += f"- {account.name}: R$ {account.balance:.2f}\n"
        report += "  Transações:\n"
        for transaction in account.get_transactions():
            report += f"    {transaction}\n"
    
    report += "Investimentos:\n"
    for investment in client.investments:
        report += f"- {investment.type}: R$ {investment.calculate_value():.2f}\n"
    
    report += f"Patrimônio Total: R$ {client.get_net_worth():.2f}\n"
    return report


# Função de Projeção de Valor Futuro
def future_value_report(client: Client, date: datetime) -> str:
    """
    Gera um relatório de projeção de valores futuros para os investimentos do cliente.

    Args:
        client (Client): O cliente para quem a projeção será gerada.
        date (datetime): A data futura para a qual os valores serão projetados.

    Returns:
        str: Um relatório formatado com a projeção dos valores futuros dos investimentos.
    """
    months_until_date = (date.year - datetime.now().year) * 12 + (date.month - datetime.now().month)
    report = f"Projeção de Investimentos para {date.strftime('%d/%m/%Y')}:\n"
    
    for investment in client.investments:
        future_value = investment.initial_amount * ((1 + investment.rate_of_return) ** months_until_date)
        report += f"- {investment.type}: R$ {future_value:.2f}\n"
    
    return report


# Exemplo de Uso
if __name__ == "__main__":
    # Criando um cliente
    cliente = Client("Ana Beatriz")

    # Criando uma conta e adicionando transações
    conta = cliente.add_account("Conta Corrente")
    conta.add_transaction(1000.0, "Depósito", "Salário")
    conta.add_transaction(-200.0, "Saída", "Compras")

    # Criando um investimento
    investimento = Investment("Ações", 5000.0, 0.05)
    cliente.add_investment(investimento)

    # Gerando o relatório financeiro
    print(generate_report(cliente))

    # Gerando a projeção de investimentos para daqui a 12 meses
    future_date = datetime(2025, 12, 31)
    print(future_value_report(cliente, future_date))

