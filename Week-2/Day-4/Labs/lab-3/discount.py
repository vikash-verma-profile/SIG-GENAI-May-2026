from __future__ import annotations


def calculate_discount(price: float, customer_type: str, is_festival: bool) -> float:
    """Calculate the final price after applying customer and festival discounts.

    Args:
        price: Original product price. Must be non-negative.
        customer_type: Customer category. Supported values: "premium", "regular".
        is_festival: Whether festival sale rules apply.

    Returns:
        Final price after applying discount rules.

    Raises:
        ValueError: If `price` is negative or `customer_type` is empty/unknown.
        TypeError: If inputs are of the wrong type.
    """
    if not isinstance(price, (int, float)):
        raise TypeError("price must be a number")
    if price < 0:
        raise ValueError("price must be non-negative")

    if not isinstance(customer_type, str) or not customer_type.strip():
        raise ValueError("customer_type must be a non-empty string")

    if not isinstance(is_festival, bool):
        raise TypeError("is_festival must be a boolean")

    customer_type = customer_type.strip().lower()

    # Premium customers receive higher discounts.
    if customer_type == "premium":
        # Extra discount during festivals.
        return float(price) * (0.7 if is_festival else 0.8)

    # Regular customers receive limited discounts.
    if customer_type == "regular":
        return float(price) * (0.9 if is_festival else 1.0)

    # Unknown customer types are treated as invalid input in production code.
    raise ValueError(f"unsupported customer_type: {customer_type!r}")


if __name__ == "__main__":
    # Quick sanity checks (not a full test suite).
    print(calculate_discount(100.0, "premium", True))   # 70.0
    print(calculate_discount(100.0, "premium", False))  # 80.0
    print(calculate_discount(100.0, "regular", True))   # 90.0
    print(calculate_discount(100.0, "regular", False))  # 100.0

