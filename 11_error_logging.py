"""Write caught exceptions to errors.log with timestamps and exception types."""

from datetime import datetime
from pathlib import Path


def log_exception(error: Exception, log_path: str | Path = "errors.log") -> None:
    """Append a timestamped exception record to the requested log file."""
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    message = str(error).replace("\r", "\\r").replace("\n", "\\n")
    record = f"{timestamp} | {type(error).__name__} | {message}\n"
    with Path(log_path).open("a", encoding="utf-8") as log_file:
        log_file.write(record)


def main() -> None:
    """Demonstrate logging a handled invalid numeric input."""
    try:
        raw_value = input("Enter a whole number: ").strip()
        try:
            value = int(raw_value)
        except ValueError as error:
            raise ValueError(f"{raw_value!r} is not a whole number.") from error
    except ValueError as error:
        print(f"Input error: {error}")
        try:
            log_exception(error)
        except PermissionError as log_error:
            print(f"Cannot write errors.log: {log_error}")
        except OSError as log_error:
            print(f"Failed to write the error log: {log_error}")
        else:
            print("The error was recorded in errors.log.")
    else:
        print(f"You entered {value}.")


if __name__ == "__main__":
    main()
