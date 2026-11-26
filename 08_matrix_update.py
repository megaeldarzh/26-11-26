"""Update a matrix element with index and value validation."""


def parse_index(value: str, field_name: str) -> int:
    """Convert an index from input, rejecting non-integer text."""
    try:
        return int(value.strip())
    except ValueError as error:
        raise ValueError(f"{field_name} must be an integer.") from error


def parse_new_value(value: str) -> int:
    """Parse an integer matrix value from input."""
    try:
        return int(value.strip())
    except ValueError as error:
        raise ValueError("The new matrix value must be an integer.") from error


def update_matrix(
    matrix: list[list[int]], row: int, column: int, new_value: int
) -> int:
    """Replace and return a matrix element, rejecting invalid indices/types."""
    if isinstance(row, bool) or not isinstance(row, int):
        raise TypeError("Row index must be an integer.")
    if isinstance(column, bool) or not isinstance(column, int):
        raise TypeError("Column index must be an integer.")
    if isinstance(new_value, bool) or not isinstance(new_value, int):
        raise TypeError("New matrix value must be an integer.")
    if row < 0 or row >= len(matrix):
        raise IndexError(f"Row index {row} is outside the matrix.")
    if column < 0 or column >= len(matrix[row]):
        raise IndexError(f"Column index {column} is outside the matrix row.")

    matrix[row][column] = new_value
    return new_value


def main() -> None:
    """Prompt for coordinates and a value in a sample matrix."""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Current matrix:")
    for matrix_row in matrix:
        print(matrix_row)

    try:
        row = parse_index(input("Row index (0-based): "), "Row index")
        column = parse_index(input("Column index (0-based): "), "Column index")
        new_value = parse_new_value(input("New integer value: "))
        update_matrix(matrix, row, column, new_value)
    except ValueError as error:
        print(f"Invalid input: {error}")
    except IndexError as error:
        print(f"Index error: {error}")
    except TypeError as error:
        print(f"Invalid value type: {error}")
    else:
        print("Updated matrix:")
        for matrix_row in matrix:
            print(matrix_row)


if __name__ == "__main__":
    main()
