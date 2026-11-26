"""In-memory inventory with product, price, quantity, and sale validation."""

import math
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class ProductNotFoundError(KeyError):
    """Raised when an inventory operation refers to an unknown product."""


class InsufficientStockError(ValueError):
    """Raised when a sale requests more items than are in stock."""


@dataclass
class Product:
    """A product held in inventory."""

    name: str
    price: Decimal
    quantity: int


def parse_price(value: str) -> Decimal:
    """Parse a strictly positive finite price."""
    try:
        price = Decimal(value.strip())
    except InvalidOperation as error:
        raise ValueError("Price must be a valid number.") from error
    if not price.is_finite() or price <= 0:
        raise ValueError("Price must be a positive finite number.")
    return price


def parse_quantity(value: str, *, allow_zero: bool = False) -> int:
    """Parse an integer quantity; sales require a positive value."""
    try:
        quantity = int(value.strip())
    except ValueError as error:
        raise ValueError("Quantity must be a whole number.") from error
    minimum = 0 if allow_zero else 1
    if quantity < minimum:
        if allow_zero:
            raise ValueError("Quantity cannot be negative.")
        raise ValueError("Quantity must be at least 1.")
    return quantity


class Inventory:
    """Store products and provide operations for stock management."""

    def __init__(self) -> None:
        self.products: dict[str, Product] = {}

    def add_product(self, name: str, price: Decimal, quantity: int) -> Product:
        """Add a product with validated name, price, and initial quantity."""
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Product name cannot be empty.")
        if clean_name in self.products:
            raise ValueError(f"Product {clean_name!r} already exists.")
        if not price.is_finite() or price <= 0:
            raise ValueError("Price must be a positive finite number.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        product = Product(clean_name, price, quantity)
        self.products[clean_name] = product
        return product

    def update_quantity(self, name: str, quantity: int) -> Product:
        """Set a product's stock quantity to a non-negative integer."""
        product = self._get_product(name)
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        product.quantity = quantity
        return product

    def sell(self, name: str, quantity: int) -> Decimal:
        """Sell the requested quantity and return the total sale amount."""
        product = self._get_product(name)
        if quantity < 1:
            raise ValueError("Sale quantity must be at least 1.")
        if quantity > product.quantity:
            raise InsufficientStockError(
                f"Only {product.quantity} unit(s) of {product.name!r} remain."
            )
        total = product.price * quantity
        if not math.isfinite(float(total)):
            raise OverflowError("The sale total is too large.")
        product.quantity -= quantity
        return total

    def list_products(self) -> list[Product]:
        """Return products in insertion order."""
        return list(self.products.values())

    def _get_product(self, name: str) -> Product:
        try:
            return self.products[name.strip()]
        except KeyError as error:
            raise ProductNotFoundError(f"Product {name!r} was not found.") from error


def main() -> None:
    """Provide a simple interactive inventory menu."""
    inventory = Inventory()
    while True:
        print("\n1) View  2) Add  3) Change quantity  4) Sell  0) Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                products = inventory.list_products()
                if not products:
                    print("Inventory is empty.")
                for product in products:
                    print(
                        f"{product.name}: price={product.price}, "
                        f"quantity={product.quantity}"
                    )
            elif choice == "2":
                name = input("Product name: ")
                price = parse_price(input("Price: "))
                quantity = parse_quantity(
                    input("Initial quantity: "), allow_zero=True
                )
                inventory.add_product(name, price, quantity)
                print("Product added.")
            elif choice == "3":
                name = input("Product name: ")
                quantity = parse_quantity(
                    input("New quantity: "), allow_zero=True
                )
                inventory.update_quantity(name, quantity)
                print("Quantity updated.")
            elif choice == "4":
                name = input("Product name: ")
                quantity = parse_quantity(input("Quantity to sell: "))
                total = inventory.sell(name, quantity)
                print(f"Sale complete. Total: {total}")
            else:
                print("Choose one of the listed options.")
        except (ValueError, ProductNotFoundError, OverflowError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
