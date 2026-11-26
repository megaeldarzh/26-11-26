"""Registration validation that reports every invalid field at once."""

from dataclasses import dataclass


class RegistrationValidationError(ValueError):
    """Raised with one or more field-specific registration messages."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


@dataclass(frozen=True)
class RegisteredUser:
    """Validated registration data."""

    name: str
    age: int
    email: str
    password: str


def parse_age(value: str) -> int:
    """Convert age input to an integer, providing a useful error message."""
    try:
        return int(value.strip())
    except ValueError as error:
        raise ValueError("Age must be a whole number.") from error


def register_user(
    name: str, age: int, email: str, password: str
) -> RegisteredUser:
    """Validate all registration fields and return a user or all errors."""
    errors: list[str] = []
    clean_name = name.strip()
    clean_email = email.strip()

    if len(clean_name) < 3:
        errors.append("Name must contain at least 3 characters.")
    if not 14 <= age <= 100:
        errors.append("Age must be between 14 and 100.")
    if "@" not in clean_email or "." not in clean_email:
        errors.append("Email must contain both '@' and '.'.")
    if len(password) < 8:
        errors.append("Password must contain at least 8 characters.")

    if errors:
        raise RegistrationValidationError(errors)
    return RegisteredUser(clean_name, age, clean_email, password)


def main() -> None:
    """Collect registration fields and display validation results."""
    name = input("Name: ")
    age_input = input("Age: ")
    email = input("Email: ")
    password = input("Password: ")

    try:
        age = parse_age(age_input)
        user = register_user(name, age, email, password)
    except RegistrationValidationError as error:
        for message in error.errors:
            print(f"Registration error: {message}")
    except ValueError as error:
        print(f"Registration error: {error}")
    else:
        print(f"Registration successful for {user.name}.")


if __name__ == "__main__":
    main()
