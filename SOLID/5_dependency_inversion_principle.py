"""
Dependency Inversion Principle (DIP)
------------------------------------
High-level modules should not depend on low-level modules.
Both should depend on abstractions.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BAD: high-level OrderService is hard-wired to a concrete MySQL class.
# Switching databases (or testing) requires editing OrderService.
# ---------------------------------------------------------------------------
class MySQLDatabase:
    def save(self, data: str):
        print(f"[MySQL] saved: {data}")


class BadOrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # tight coupling

    def place_order(self, order: str):
        self.db.save(order)


# ---------------------------------------------------------------------------
# GOOD: depend on an abstraction; inject the concrete implementation.
# ---------------------------------------------------------------------------
class Database(ABC):
    @abstractmethod
    def save(self, data: str): ...


class MySQL(Database):
    def save(self, data: str):
        print(f"[MySQL] saved: {data}")


class MongoDB(Database):
    def save(self, data: str):
        print(f"[MongoDB] saved: {data}")


class InMemoryDB(Database):
    """Handy for tests."""

    def __init__(self):
        self.records = []

    def save(self, data: str):
        self.records.append(data)


class OrderService:
    def __init__(self, db: Database):  # dependency injected
        self.db = db

    def place_order(self, order: str):
        self.db.save(order)


if __name__ == "__main__":
    OrderService(MySQL()).place_order("order-1")
    OrderService(MongoDB()).place_order("order-2")

    test_db = InMemoryDB()
    OrderService(test_db).place_order("order-3")
    print(test_db.records)
