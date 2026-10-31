"""
Unit tests for inventory stock management and deduction invariants.
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.core.inventory import InventoryManager


def test_inventory_stock_lifecycle():
    inv = InventoryManager()
    inv.set_stock("SKU-LAPTOP", 10)
    assert inv.get_stock("SKU-LAPTOP") == 10

    remaining = inv.deduct("SKU-LAPTOP", 3)
    assert remaining == 7
    assert inv.get_stock("SKU-LAPTOP") == 7

    restocked = inv.restock("SKU-LAPTOP", 5)
    assert restocked == 12
    assert inv.get_stock("SKU-LAPTOP") == 12


def test_inventory_insufficient_stock():
    inv = InventoryManager()
    inv.set_stock("SKU-GPU", 2)
    with pytest.raises(RuntimeError, match="Insufficient stock for SKU 'SKU-GPU'"):
        inv.deduct("SKU-GPU", 5)


def test_inventory_boundary_validations():
    inv = InventoryManager()
    with pytest.raises(ValueError, match="Stock count cannot be negative"):
        inv.set_stock("SKU-FAIL", -1)
    with pytest.raises(ValueError, match="Deduction quantity must be positive"):
        inv.deduct("SKU-FAIL", 0)
    with pytest.raises(ValueError, match="Restock quantity must be positive"):
        inv.restock("SKU-FAIL", -5)
