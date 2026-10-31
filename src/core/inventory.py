"""
Inventory Allocation Service with Mutation Guarding and Stock Tracking.
Author: Saksham Singh (24BTRAO035)
"""
from typing import Dict


class InventoryManager:
    """
    Maintains inventory levels, enforces invariants against negative stock,
    and supports multi-item batch deductions.
    """
    def __init__(self):
        self._stock: Dict[str, int] = {}

    def set_stock(self, sku: str, count: int) -> int:
        if count < 0:
            raise ValueError(f"Stock count cannot be negative: {count}")
        self._stock[sku] = count
        return self._stock[sku]

    def get_stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def deduct(self, sku: str, count: int) -> int:
        if count <= 0:
            raise ValueError("Deduction quantity must be positive")
        current = self.get_stock(sku)
        if current < count:
            raise RuntimeError(f"Insufficient stock for SKU '{sku}': available {current}, requested {count}")
        self._stock[sku] = current - count
        return self._stock[sku]

    def restock(self, sku: str, count: int) -> int:
        if count <= 0:
            raise ValueError("Restock quantity must be positive")
        self._stock[sku] = self.get_stock(sku) + count
        return self._stock[sku]
