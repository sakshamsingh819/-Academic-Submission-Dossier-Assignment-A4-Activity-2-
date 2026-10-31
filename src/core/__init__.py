"""
Business domain modules for e-commerce computation.
"""
from .pricing import apply_discount, add_tax, calculate_final_price
from .cart import ShoppingCart, CartItem
from .inventory import InventoryManager

__all__ = [
    "apply_discount",
    "add_tax",
    "calculate_final_price",
    "ShoppingCart",
    "CartItem",
    "InventoryManager",
]
