"""
Interface Segregation Principle (ISP)
-------------------------------------
Clients should not be forced to depend on methods they do not use.
Prefer several small, focused interfaces over one fat interface.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BAD: one fat interface forces BasicPrinter to implement scan/fax it can't do.
# ---------------------------------------------------------------------------
class BadMachine(ABC):
    @abstractmethod
    def print(self, doc: str): ...

    @abstractmethod
    def scan(self, doc: str): ...

    @abstractmethod
    def fax(self, doc: str): ...


class BadBasicPrinter(BadMachine):
    def print(self, doc: str):
        print(f"Printing {doc}")

    def scan(self, doc: str):
        raise NotImplementedError  # forced, meaningless

    def fax(self, doc: str):
        raise NotImplementedError  # forced, meaningless


# ---------------------------------------------------------------------------
# GOOD: small interfaces; classes implement only what they support.
# ---------------------------------------------------------------------------
class Printer(ABC):
    @abstractmethod
    def print(self, doc: str): ...


class Scanner(ABC):
    @abstractmethod
    def scan(self, doc: str): ...


class Fax(ABC):
    @abstractmethod
    def fax(self, doc: str): ...


class BasicPrinter(Printer):
    def print(self, doc: str):
        print(f"Printing {doc}")


class MultiFunctionMachine(Printer, Scanner, Fax):
    def print(self, doc: str):
        print(f"Printing {doc}")

    def scan(self, doc: str):
        print(f"Scanning {doc}")

    def fax(self, doc: str):
        print(f"Faxing {doc}")


def scan_document(scanner: Scanner, doc: str):
    scanner.scan(doc)  # depends only on what it needs


if __name__ == "__main__":
    BasicPrinter().print("report.pdf")

    mfm = MultiFunctionMachine()
    mfm.print("report.pdf")
    scan_document(mfm, "report.pdf")
    mfm.fax("report.pdf")
