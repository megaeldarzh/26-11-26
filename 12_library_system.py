"""A small JSON-backed library with explicit book and file error handling."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class BookNotFoundError(KeyError):
    """Raised when a book title is not in the library."""


class BookAlreadyExistsError(ValueError):
    """Raised when trying to add a title that is already in the library."""


class BookAlreadyBorrowedError(ValueError):
    """Raised when a borrowed book is requested again."""


class BookNotBorrowedError(ValueError):
    """Raised when attempting to return a book that is not borrowed."""


class InvalidLibraryDataError(ValueError):
    """Raised when the library file is malformed or has an invalid schema."""


@dataclass
class Book:
    """A book's identifying details and availability state."""

    title: str
    author: str
    borrowed: bool = False


class Library:
    """Manage a collection of books and persist it as a JSON document."""

    def __init__(self) -> None:
        self.books: dict[str, Book] = {}

    @staticmethod
    def _key(title: str) -> str:
        return title.strip().casefold()

    def add_book(self, title: str, author: str) -> Book:
        """Add a book after validating its title and author."""
        clean_title = title.strip()
        clean_author = author.strip()
        if not clean_title:
            raise ValueError("Book title cannot be empty.")
        if not clean_author:
            raise ValueError("Author cannot be empty.")
        key = self._key(clean_title)
        if key in self.books:
            raise BookAlreadyExistsError(
                f"Book {clean_title!r} is already in the library."
            )
        book = Book(clean_title, clean_author)
        self.books[key] = book
        return book

    def search_book(self, title: str) -> Book:
        """Find a book by title, ignoring surrounding whitespace and case."""
        key = self._key(title)
        try:
            return self.books[key]
        except KeyError as error:
            raise BookNotFoundError(f"Book {title!r} was not found.") from error

    def borrow_book(self, title: str) -> Book:
        """Mark an available book as borrowed."""
        book = self.search_book(title)
        if book.borrowed:
            raise BookAlreadyBorrowedError(
                f"Book {book.title!r} has already been borrowed."
            )
        book.borrowed = True
        return book

    def return_book(self, title: str) -> Book:
        """Mark a borrowed book as available."""
        book = self.search_book(title)
        if not book.borrowed:
            raise BookNotBorrowedError(
                f"Book {book.title!r} is not currently borrowed."
            )
        book.borrowed = False
        return book

    def save(self, file_path: str | Path) -> None:
        """Serialize all books to a UTF-8 JSON file."""
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "borrowed": book.borrowed,
                }
                for book in self.books.values()
            ]
        }
        with Path(file_path).open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")

    @classmethod
    def load(cls, file_path: str | Path) -> "Library":
        """Load and validate a library JSON file; file access errors propagate."""
        try:
            with Path(file_path).open("r", encoding="utf-8") as file:
                data: Any = json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidLibraryDataError(
                f"Invalid JSON at line {error.lineno}, column {error.colno}: "
                f"{error.msg}"
            ) from error
        except UnicodeDecodeError as error:
            raise InvalidLibraryDataError(
                f"Library file is not valid UTF-8: {error}"
            ) from error

        if not isinstance(data, dict) or not isinstance(data.get("books"), list):
            raise InvalidLibraryDataError(
                "Library file must contain a 'books' list."
            )

        library = cls()
        for index, item in enumerate(data["books"], start=1):
            if not isinstance(item, dict):
                raise InvalidLibraryDataError(
                    f"Book entry {index} must be a JSON object."
                )
            title = item.get("title")
            author = item.get("author")
            borrowed = item.get("borrowed")
            if (
                not isinstance(title, str)
                or not title.strip()
                or not isinstance(author, str)
                or not author.strip()
                or not isinstance(borrowed, bool)
            ):
                raise InvalidLibraryDataError(
                    f"Book entry {index} has invalid title, author, or borrowed status."
                )
            try:
                book = library.add_book(title, author)
            except ValueError as error:
                raise InvalidLibraryDataError(
                    f"Book entry {index} is invalid: {error}"
                ) from error
            book.borrowed = borrowed
        return library


def _show_books(library: Library) -> None:
    """Print all books or an explicit empty-library message."""
    if not library.books:
        print("The library is empty.")
        return
    for book in library.books.values():
        status = "borrowed" if book.borrowed else "available"
        print(f"{book.title} — {book.author} [{status}]")


def _run_menu(library: Library) -> None:
    """Handle user operations until the user chooses to exit."""
    while True:
        print("\n1) Add  2) Search  3) Borrow  4) Return  5) List  0) Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                book = library.add_book(
                    input("Title: "),
                    input("Author: "),
                )
                print(f"Added {book.title!r}.")
            elif choice == "2":
                book = library.search_book(input("Title to find: "))
                print(f"{book.title} — {book.author}; borrowed={book.borrowed}.")
            elif choice == "3":
                book = library.borrow_book(input("Title to borrow: "))
                print(f"You borrowed {book.title!r}.")
            elif choice == "4":
                book = library.return_book(input("Title to return: "))
                print(f"You returned {book.title!r}.")
            elif choice == "5":
                _show_books(library)
            else:
                print("Choose one of the listed options.")
        except BookNotFoundError as error:
            print(f"Book not found: {error}")
        except (BookAlreadyExistsError, BookAlreadyBorrowedError) as error:
            print(f"Book operation failed: {error}")
        except (BookNotBorrowedError, ValueError) as error:
            print(f"Invalid operation: {error}")


def main() -> None:
    """Load the library on startup, run the menu, and save on exit."""
    storage_path = Path(__file__).with_name("library.json")
    try:
        library = Library.load(storage_path)
    except FileNotFoundError:
        library = Library()
        print("No saved library found; starting with an empty collection.")
    except PermissionError as error:
        print(f"Cannot access the library file: {error}")
        return
    except InvalidLibraryDataError as error:
        print(f"Library file is damaged: {error}")
        return
    except OSError as error:
        print(f"Could not load the library: {error}")
        return
    else:
        print(f"Loaded {len(library.books)} book(s).")

    try:
        _run_menu(library)
    finally:
        try:
            library.save(storage_path)
        except PermissionError as error:
            print(f"Permission denied while saving the library: {error}")
        except OSError as error:
            print(f"Could not save the library: {error}")
        else:
            print("Library saved.")


if __name__ == "__main__":
    main()
