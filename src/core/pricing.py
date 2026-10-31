"""
Pricing Calculation Module with Deterministic Business Rules.
Author: Saksham Singh (24BTRAO035)
"""

def apply_discount(price: float, percent: float) -> float:
    """
    Applies percentage discount to a given price.
    Validates boundary conditions: 0 <= percent <= 100.
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not (0 <= percent <= 100):
        raise ValueError("Discount percent must be between 0 and 100")
    discounted = price * (1.0 - (percent / 100.0))
    return round(discounted, 2)


def add_tax(price: float, rate: float = 0.18) -> float:
    """
    Applies standard taxation (default 18% GST).
    Validates non-negative inputs.
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if rate < 0:
        raise ValueError("Tax rate cannot be negative")
    return round(price * (1.0 + rate), 2)


def calculate_final_price(base_price: float, discount_pct: float, tax_rate: float = 0.18) -> float:
    """
    Orchestrates discount application followed by tax evaluation.
    """
    discounted = apply_discount(base_price, discount_pct)
    return add_tax(discounted, tax_rate)
