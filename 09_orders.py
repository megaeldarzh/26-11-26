"""Create orders while checking stock and a maximum order total."""

import math
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class ProductNotFoundError(KeyError):
    """Raised when an order references a product not in the catalog."""


class InvalidQuantityError(ValueError):
    """Raised when the requested order quantity is not a positive integer."""


class InsufficientStockError(ValueError):
    """Raised when requested quantity exceeds the available stock."""


class OrderLimitExceededError(ValueError):
    """Raised when an order total exceeds the configured limit."""


@dataclass
class OrderProduct:
    """A product with a price and currently available stock."""

    name: str
    price: Decimal
    quantity: int


@dataclass(frozen=True)
class Order:
    """A successfully accepted order."""

    product_name: str
    quantity: int
    total: Decimal


def parse_quantity(value: str) -> int:
    """Parse a positive integer quantity from console input."""
    try:
        quantity = int(value.strip())
    except ValueError as error:
        raise InvalidQuantityError("Quantity must be a whole number.") from error
    if quantity < 1:
        raise InvalidQuantityError("Quantity must be at least 1.")
    return quantity


def parse_price(value: str) -> Decimal:
    """Parse a positive finite product price."""
    try:
        price = Decimal(value.strip())
    except InvalidOperation as error:
        raise ValueError("Price must be a valid number.") from error
    if not price.is_finite() or price <= 0:
        raise ValueError("Price must be a positive finite number.")
    return price


class OrderService:
    """Validate orders and decrement stock only after all checks pass."""

    def __init__(
        self, products: dict[str, OrderProduct], order_limit: Decimal
    ) -> None:
        if not order_limit.is_finite() or order_limit <= 0:
            raise ValueError("Order limit must be a positive finite amount.")
        self.products = products
        self.order_limit = order_limit

    def create_order(self, product_name: str, quantity: int) -> Order:
        """Create an order or raise a specific validation exception."""
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise InvalidQuantityError("Quantity must be a positive integer.")
        try:
            product = self.products[product_name.strip()]
        except KeyError as error:
            raise ProductNotFoundError(
                f"Product {product_name!r} was not found."
            ) from error

        if quantity > product.quantity:
            raise InsufficientStockError(
                f"Only {product.quantity} unit(s) of {product.name!r} are available."
            )
        total = product.price * quantity
        if not math.isfinite(float(total)):
            raise OverflowError("The order total is too large to represent.")
        if total > self.order_limit:
            raise OrderLimitExceededError(
                f"Order total {total} exceeds the limit {self.order_limit}."
            )

        product.quantity -= quantity
        return Order(product.name, quantity, total)


def main() -> None:
    """Collect a product and quantity, then create one sample order."""
    products = {
        "notebook": OrderProduct("notebook", Decimal("12.50"), 20),
        "headphones": OrderProduct("headphones", Decimal("89.99"), 5),
    }
    service = OrderService(products, Decimal("500.00"))

    print("Available products:")
    for product in products.values():
        print(f"{product.name}: {product.price} ({product.quantity} in stock)")

    try:
        product_name = input("Product name: ").strip()
        quantity = parse_quantity(input("Quantity: "))
        order = service.create_order(product_name, quantity)
    except ProductNotFoundError as error:
        print(f"Order failed: {error}")
    except InvalidQuantityError as error:
        print(f"Invalid quantity: {error}")
    except InsufficientStockError as error:
        print(f"Not enough stock: {error}")
    except OrderLimitExceededError as error:
        print(f"Order limit exceeded: {error}")
    except OverflowError as error:
        print(f"Order failed: {error}")
    else:
        print(
            f"Order accepted: {order.quantity} x {order.product_name}; "
            f"total {order.total}."
        )


if __name__ == "__main__":
    main()
