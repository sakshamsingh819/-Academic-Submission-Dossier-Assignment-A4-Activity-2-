"""
Shopping Cart Management Module with Itemization and Aggregation.
Author: Saksham Singh (24BTRAO035)
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CartItem:
    sku: str
    name: str
    price: float
    quantity: int

    def item_total(self) -> float:
        return round(self.price * self.quantity, 2)


class ShoppingCart:
    """
    Manages in-session shopping cart aggregations, threshold discounts, and item validations.
    """
    def __init__(self):
        self._items: Dict[str, CartItem] = {}

    def add_item(self, sku: str, name: str, price: float, quantity: int = 1) -> CartItem:
        if price <= 0:
            raise ValueError(f"Price must be strictly positive: {price}")
        if quantity <= 0:
            raise ValueError(f"Quantity must be strictly positive: {quantity}")

        if sku in self._items:
            existing = self._items[sku]
            self._items[sku] = CartItem(
                sku=sku,
                name=name,
                price=price,
                quantity=existing.quantity + quantity
            )
        else:
            self._items[sku] = CartItem(sku=sku, name=name, price=price, quantity=quantity)
        return self._items[sku]

    def remove_item(self, sku: str) -> bool:
        if sku in self._items:
            del self._items[sku]
            return True
        return False

    def get_items(self) -> List[CartItem]:
        return list(self._items.values())

    def item_count(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def subtotal(self) -> float:
        total = sum(item.item_total() for item in self._items.values())
        return round(total, 2)

    def clear(self) -> None:
        self._items.clear()
