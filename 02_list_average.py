"""Parse space-separated numbers and calculate their arithmetic mean."""

import math


def parse_numbers(text: str) -> list[float]:
    """Parse space-separated finite numbers, rejecting empty or invalid input."""
    tokens = text.split()
    if not tokens:
        raise ValueError("The list is empty; enter at least one number.")

    numbers: list[float] = []
    for token in tokens:
        try:
            number = float(token)
        except ValueError as error:
            raise ValueError(f"{token!r} is not a valid number.") from error
        if not math.isfinite(number):
            raise ValueError(f"{token!r} is not a finite number.")
        numbers.append(number)
    return numbers


def calculate_average(numbers: list[float]) -> float:
    """Return the average, raising ValueError when it cannot be calculated."""
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list.")
    if any(not math.isfinite(number) for number in numbers):
        raise ValueError("All values must be finite numbers.")

    try:
        average = math.fsum(numbers) / len(numbers)
    except OverflowError as error:
        raise ValueError("The values are too large to calculate an average.") from error
    if not math.isfinite(average):
        raise ValueError("The values are too large to calculate an average.")
    return average


def main() -> None:
    """Run the interactive average-calculation example."""
    try:
        numbers = parse_numbers(input("Enter numbers separated by spaces: "))
        average = calculate_average(numbers)
    except ValueError as error:
        print(f"Cannot calculate the average: {error}")
    else:
        print(f"Average: {average:g}")


if __name__ == "__main__":
    main()
