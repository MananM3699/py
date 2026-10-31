"""
Single Responsibility Principle (SRP)
-------------------------------------
A class should have only one reason to change.
"""


# ---------------------------------------------------------------------------
# BAD: Invoice does calculation, printing and persistence.
# A change in tax rules, print format, or storage all force edits to this class.
# ---------------------------------------------------------------------------
class BadInvoice:
    def __init__(self, items):
        self.items = items  # list of (name, price, qty)

    def calculate_total(self):
        return sum(price * qty for _, price, qty in self.items)

    def print_invoice(self):
        print("INVOICE")
        for name, price, qty in self.items:
            print(f"{name} x{qty} @ {price}")
        print(f"Total: {self.calculate_total()}")

    def save_to_file(self, path):
        with open(path, "w") as f:
            f.write(f"Total: {self.calculate_total()}")


# ---------------------------------------------------------------------------
# GOOD: each class has exactly one responsibility.
# ---------------------------------------------------------------------------
class Invoice:
    """Holds invoice data and business calculation only."""

    def __init__(self, items):
        self.items = items  # list of (name, price, qty)

    def calculate_total(self):
        return sum(price * qty for _, price, qty in self.items)


class InvoicePrinter:
    """Responsible only for presentation."""

    def print(self, invoice: Invoice):
        print("INVOICE")
        for name, price, qty in invoice.items:
            print(f"{name} x{qty} @ {price}")
        print(f"Total: {invoice.calculate_total()}")


class InvoiceRepository:
    """Responsible only for persistence."""

    def save_to_file(self, invoice: Invoice, path: str):
        with open(path, "w") as f:
            f.write(f"Total: {invoice.calculate_total()}")


if __name__ == "__main__":
    invoice = Invoice([("Book", 250, 2), ("Pen", 10, 5)])

    InvoicePrinter().print(invoice)
    InvoiceRepository().save_to_file(invoice, "invoice.txt")
