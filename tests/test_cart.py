"""
Unit tests for shopping cart management and aggregations.
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.core.cart import ShoppingCart


def test_cart_initial_state():
    cart = ShoppingCart()
    assert cart.item_count() == 0
    assert cart.subtotal() == 0.0


def test_cart_add_and_aggregate():
    cart = ShoppingCart()
    cart.add_item("SKU-1", "Mechanical Keyboard", 100.0, 2)
    cart.add_item("SKU-2", "Ergonomic Mouse", 50.0, 1)

    assert cart.item_count() == 3
    assert cart.subtotal() == 250.00


def test_cart_incremental_quantity():
    cart = ShoppingCart()
    cart.add_item("SKU-1", "Desk Mat", 20.0, 1)
    cart.add_item("SKU-1", "Desk Mat", 20.0, 2)

    assert cart.item_count() == 3
    assert cart.subtotal() == 60.00


def test_cart_remove_item():
    cart = ShoppingCart()
    cart.add_item("SKU-1", "USB Cable", 10.0, 1)
    assert cart.remove_item("SKU-1") is True
    assert cart.remove_item("SKU-NONEXISTENT") is False
    assert cart.item_count() == 0


def test_cart_invalid_inputs():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Price must be strictly positive"):
        cart.add_item("SKU-ERR", "Free Item", 0.0, 1)
    with pytest.raises(ValueError, match="Quantity must be strictly positive"):
        cart.add_item("SKU-ERR", "Normal Item", 10.0, 0)
