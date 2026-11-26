"""A command-line calculator with input and result-size validation."""

import math
from collections.abc import Callable


MAX_RESULT_ABS = 1e100
OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": lambda left, right: left + right,
    "-": lambda left, right: left - right,
    "*": lambda left, right: left * right,
    "/": lambda left, right: left / right,
    "//": lambda left, right: left // right,
    "%": lambda left, right: left % right,
    "**": lambda left, right: left**right,
}


def parse_number(value: str, field_name: str) -> float:
    """Parse a finite floating-point number from user input."""
    try:
        number = float(value.strip())
    except ValueError as error:
        raise ValueError(f"{field_name} must be a valid number.") from error
    if not math.isfinite(number):
        raise ValueError(f"{field_name} must be finite.")
    return number


def calculate(left: float, operator: str, right: float) -> float:
    """Calculate a result or raise a specific error for invalid operations."""
    if operator not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operator!r}.")
    if not math.isfinite(left) or not math.isfinite(right):
        raise ValueError("Operands must be finite numbers.")

    try:
        result = OPERATIONS[operator](left, right)
    except ZeroDivisionError:
        raise
    except OverflowError as error:
        raise OverflowError("The result is too large.") from error

    if not math.isfinite(result) or abs(result) > MAX_RESULT_ABS:
        raise OverflowError(
            f"The result exceeds the supported size ({MAX_RESULT_ABS:g})."
        )
    return result


def main() -> None:
    """Read two operands and an operation, then display the result."""
    try:
        left = parse_number(input("First number: "), "First number")
        operator = input("Operation (+, -, *, /, //, %, **): ").strip()
        right = parse_number(input("Second number: "), "Second number")
        result = calculate(left, operator, right)
    except ValueError as error:
        print(f"Invalid input: {error}")
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    except OverflowError as error:
        print(f"Calculation failed: {error}")
    else:
        print(f"Result: {result:g}")


if __name__ == "__main__":
    main()
