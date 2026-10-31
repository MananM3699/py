"""
Liskov Substitution Principle (LSP)
-----------------------------------
Subclasses must be usable wherever their base class is expected,
without breaking the correctness of the program.
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# BAD: Penguin "is a" Bird, but cannot fly -> breaks code that expects flying.
# ---------------------------------------------------------------------------
class BadBird:
    def fly(self):
        return "Flying"


class BadPenguin(BadBird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly")  # violates the contract


def bad_make_it_fly(bird: BadBird):
    return bird.fly()  # crashes for BadPenguin


# ---------------------------------------------------------------------------
# GOOD: model capabilities separately so every subtype honours its contract.
# ---------------------------------------------------------------------------
class Bird(ABC):
    @abstractmethod
    def eat(self) -> str: ...


class FlyingBird(Bird):
    @abstractmethod
    def fly(self) -> str: ...


class Sparrow(FlyingBird):
    def eat(self) -> str:
        return "Sparrow eating"

    def fly(self) -> str:
        return "Sparrow flying"


class Penguin(Bird):
    def eat(self) -> str:
        return "Penguin eating"


def make_it_fly(bird: FlyingBird) -> str:
    return bird.fly()  # safe for every FlyingBird


def feed(bird: Bird) -> str:
    return bird.eat()  # safe for every Bird, including Penguin


if __name__ == "__main__":
    print(make_it_fly(Sparrow()))
    print(feed(Sparrow()))
    print(feed(Penguin()))
