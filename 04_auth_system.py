"""A small authentication example with a three-attempt lockout."""


class InvalidCredentialsError(ValueError):
    """Raised when a login field is empty or credentials do not match."""


class AccountLockedError(RuntimeError):
    """Raised when all authentication attempts have been used."""


class Authenticator:
    """Authenticate users and lock the current session after failed attempts."""

    def __init__(self, users: dict[str, str], max_attempts: int = 3) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        self._users = users.copy()
        self.max_attempts = max_attempts
        self.failed_attempts = 0
        self.is_locked = False

    def authenticate(self, username: str, password: str) -> bool:
        """Return True for valid credentials; otherwise raise a clear error."""
        if self.is_locked:
            raise AccountLockedError("Login is locked after too many failures.")

        if not username.strip() or not password:
            reason = "Username and password cannot be empty."
        elif username not in self._users:
            reason = f"Unknown username: {username!r}."
        elif self._users[username] != password:
            reason = "Incorrect password."
        else:
            self.failed_attempts = 0
            return True

        self.failed_attempts += 1
        if self.failed_attempts >= self.max_attempts:
            self.is_locked = True
            raise AccountLockedError(
                f"{reason} Login is now locked after "
                f"{self.max_attempts} failed attempts."
            )
        raise InvalidCredentialsError(
            f"{reason} Attempts remaining: "
            f"{self.max_attempts - self.failed_attempts}."
        )


def main() -> None:
    """Run the interactive login example."""
    authenticator = Authenticator({"student": "python123"})
    while not authenticator.is_locked:
        username = input("Username: ")
        password = input("Password: ")
        try:
            authenticator.authenticate(username, password)
        except AccountLockedError as error:
            print(error)
        except InvalidCredentialsError as error:
            print(error)
        else:
            print("Login successful.")
            return


if __name__ == "__main__":
    main()
