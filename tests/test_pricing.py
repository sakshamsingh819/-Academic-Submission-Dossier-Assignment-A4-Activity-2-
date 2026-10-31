"""
Unit tests for pricing calculations and boundary validations.
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.core.pricing import apply_discount, add_tax, calculate_final_price


def test_discount_basic():
    assert apply_discount(100.0, 10.0) == 90.00
    assert apply_discount(250.0, 20.0) == 200.00


def test_discount_boundary_limits():
    assert apply_discount(100.0, 0.0) == 100.00
    assert apply_discount(100.0, 100.0) == 0.00


def test_discount_invalid_percent():
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        apply_discount(100.0, -5.0)
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        apply_discount(100.0, 105.0)


def test_discount_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        apply_discount(-50.0, 10.0)


def test_tax_calculation():
    assert add_tax(100.0, 0.18) == 118.00
    assert add_tax(100.0, 0.0) == 100.00


def test_tax_negative_inputs():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        add_tax(-100.0, 0.18)
    with pytest.raises(ValueError, match="Tax rate cannot be negative"):
        add_tax(100.0, -0.05)


def test_calculate_final_price():
    # Base 200, 10% discount -> 180, 18% tax on 180 = 212.40
    assert calculate_final_price(200.0, 10.0, 0.18) == 212.40
