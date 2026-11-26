"""Registration example using three dedicated exception types."""


class InvalidAgeError(Exception):
    """Raised when an age is outside the permitted registration range."""


class InvalidEmailError(Exception):
    """Raised when an email does not contain the required characters."""


class WeakPasswordError(Exception):
    """Raised when a password is shorter than the minimum length."""


def register_user(name: str, age: int, email: str, password: str) -> str:
    """Validate registration fields and return the normalized user's name."""
    clean_name = name.strip()
    if len(clean_name) < 3:
        raise ValueError("Name must contain at least 3 characters.")
    if not 14 <= age <= 100:
        raise InvalidAgeError("Age must be between 14 and 100.")
    clean_email = email.strip()
    if "@" not in clean_email or "." not in clean_email:
        raise InvalidEmailError("Email must contain both '@' and '.'.")
    if len(password) < 8:
        raise WeakPasswordError("Password must contain at least 8 characters.")
    return clean_name


def main() -> None:
    """Collect registration details and handle each custom error separately."""
    name = input("Name: ")
    age_input = input("Age: ")
    email = input("Email: ")
    password = input("Password: ")

    try:
        age = int(age_input.strip())
        user_name = register_user(name, age, email, password)
    except ValueError as error:
        print(f"Invalid input: {error}")
    except InvalidAgeError as error:
        print(f"Age error: {error}")
    except InvalidEmailError as error:
        print(f"Email error: {error}")
    except WeakPasswordError as error:
        print(f"Password error: {error}")
    else:
        print(f"Registration successful for {user_name}.")


if __name__ == "__main__":
    main()
