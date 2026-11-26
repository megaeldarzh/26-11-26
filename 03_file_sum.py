"""Read one number per line from a file and calculate their sum."""

import math
from pathlib import Path


class InvalidNumberLineError(ValueError):
    """Raised when a file line cannot be parsed as a finite number."""

    def __init__(self, line_number: int, value: str, reason: str) -> None:
        self.line_number = line_number
        self.value = value
        self.reason = reason
        super().__init__(
            f"Line {line_number}: {value!r} is invalid ({reason})."
        )


def read_numbers(file_path: str | Path) -> list[float]:
    """Read finite numeric values, reporting the line for malformed input."""
    numbers: list[float] = []
    with Path(file_path).open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            value = raw_line.strip()
            if not value:
                continue
            try:
                number = float(value)
            except ValueError as error:
                raise InvalidNumberLineError(
                    line_number, value, "not a valid number"
                ) from error
            if not math.isfinite(number):
                raise InvalidNumberLineError(
                    line_number, value, "number must be finite"
                )
            numbers.append(number)
    return numbers


def sum_file_numbers(file_path: str | Path) -> float:
    """Return the sum of all numbers in a file."""
    numbers = read_numbers(file_path)
    try:
        return math.fsum(numbers)
    except OverflowError as error:
        raise OverflowError("The sum is too large to represent.") from error


def main() -> None:
    """Read a file name, sum its values, and report common file errors."""
    file_name = input("File name [numbers.txt]: ").strip() or "numbers.txt"
    try:
        total = sum_file_numbers(file_name)
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except PermissionError:
        print(f"Permission denied while reading: {file_name}")
    except InvalidNumberLineError as error:
        print(f"Invalid file content: {error}")
    except OverflowError as error:
        print(f"Cannot calculate the sum: {error}")
    except OSError as error:
        print(f"Could not read {file_name}: {error}")
    else:
        print(f"Sum: {total:g}")


if __name__ == "__main__":
    main()
