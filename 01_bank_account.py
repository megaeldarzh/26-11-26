"""Bank account example with explicit input and transaction validation."""

from decimal import Decimal, InvalidOperation


class InsufficientFundsError(ValueError):
    """Raised when a withdrawal exceeds the available balance."""


def parse_amount(value: str, field_name: str) -> Decimal:
    """Convert user input to a finite Decimal amount."""
    try:
        amount = Decimal(value.strip())
    except InvalidOperation as error:
        raise ValueError(f"{field_name}: enter a valid number.") from error

    if not amount.is_finite():
        raise ValueError(f"{field_name}: the amount must be finite.")
    return amount


class BankAccount:
    """A simple account that supports deposits and withdrawals."""

    def __init__(self, balance: Decimal = Decimal("0")) -> None:
        if not balance.is_finite():
            raise ValueError("The initial balance must be finite.")
        if balance < 0:
            raise ValueError("The initial balance cannot be negative.")
        self.balance = balance

    def deposit(self, amount: Decimal) -> Decimal:
        """Add a non-negative amount and return the new balance."""
        self._validate_amount(amount)
        self.balance += amount
        return self.balance

    def withdraw(self, amount: Decimal) -> Decimal:
        """Withdraw an amount, or raise if it is negative or unaffordable."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance is {self.balance}, "
                f"requested {amount}."
            )
        self.balance -= amount
        return self.balance

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if not amount.is_finite():
            raise ValueError("The amount must be finite.")
        if amount < 0:
            raise ValueError("The amount cannot be negative.")


def main() -> None:
    """Run the interactive bank-account example."""
    try:
        initial_balance = parse_amount(input("Initial balance: "), "Balance")
        account = BankAccount(initial_balance)
        amount = parse_amount(input("Withdrawal amount: "), "Amount")
        new_balance = account.withdraw(amount)
    except InsufficientFundsError as error:
        print(f"Transaction declined: {error}")
    except ValueError as error:
        print(f"Invalid input: {error}")
    else:
        print(f"Withdrawal successful. Balance: {new_balance}")


if __name__ == "__main__":
    main()
