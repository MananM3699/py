"""
Open/Closed Principle (OCP)
---------------------------
Software entities should be open for extension but closed for modification.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BAD: adding a new discount type means editing this function (if/elif chain).
# ---------------------------------------------------------------------------
def bad_discount(customer_type: str, amount: float) -> float:
    if customer_type == "regular":
        return amount * 0.95
    elif customer_type == "premium":
        return amount * 0.90
    return amount


# ---------------------------------------------------------------------------
# GOOD: new discounts are added by creating new classes; nothing existing changes.
# ---------------------------------------------------------------------------
class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float: ...


class RegularDiscount(Discount):
    def apply(self, amount: float) -> float:
        return amount * 0.95


class PremiumDiscount(Discount):
    def apply(self, amount: float) -> float:
        return amount * 0.90


# Extension: added later without touching any code above or in Checkout.
class FestivalDiscount(Discount):
    def apply(self, amount: float) -> float:
        return amount * 0.80


class Checkout:
    def total(self, amount: float, discount: Discount) -> float:
        return discount.apply(amount)


if __name__ == "__main__":
    checkout = Checkout()
    print(checkout.total(1000, RegularDiscount()))   # 950.0
    print(checkout.total(1000, PremiumDiscount()))   # 900.0
    print(checkout.total(1000, FestivalDiscount()))  # 800.0
