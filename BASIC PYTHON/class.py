"""
Classes, Abstract Classes and Interfaces in Python
===================================================

1. CLASS
   A blueprint for creating objects. It bundles data (attributes) and
   behaviour (methods) together. An object is an instance of a class.

2. ABSTRACT CLASS
   A class that cannot be instantiated directly. It exists to be subclassed.
   It can contain:
     - abstract methods  : declared but NOT implemented; subclasses MUST override
     - concrete methods  : normal, shared implementation reused by subclasses
     - attributes / __init__ : shared state
   Use it when subclasses share common code AND must follow a common contract
   ("is-a" relationship with partial implementation).
   Python implements this with the `abc` module (ABC + @abstractmethod).

3. INTERFACE
   A pure contract: only method signatures, no implementation and no state.
   Any class that "implements" it promises to provide those methods.
   Python has no `interface` keyword, so we get one in two ways:
     a) An abstract class with ONLY abstract methods (explicit, nominal).
     b) typing.Protocol (structural / "duck typing" - a class satisfies the
        interface just by having the right methods, no inheritance needed).
   Use it when unrelated classes need to be used interchangeably
   ("can-do" relationship), e.g. Flyable, Swimmable, Comparable.

Quick comparison
----------------
| Feature              | Class         | Abstract Class        | Interface           |
|----------------------|---------------|-----------------------|---------------------|
| Instantiate directly | Yes           | No                    | No                  |
| Concrete methods     | Yes           | Yes (mixed)           | No (signatures only)|
| State (attributes)   | Yes           | Yes                   | No                  |
| Multiple inheritance | Yes           | Yes                   | Yes (commonly used) |
| Purpose              | Create object | Shared base + contract| Pure contract       |
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# 1. CLASS
# ---------------------------------------------------------------------------
class Person:
    species = "Homo sapiens"  # class attribute: shared by all instances

    def __init__(self, name: str, age: int):
        # instance attributes: unique to each object
        self.name = name
        self.age = age

    def greet(self) -> str:  # instance method
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int, current_year: int = 2026):
        # alternative constructor; receives the class itself (cls)
        return cls(name, current_year - birth_year)

    @staticmethod
    def is_adult(age: int) -> bool:
        # utility function; needs neither self nor cls
        return age >= 18


def demo_class():
    print("--- CLASS ---")
    p = Person("Chirag", 25)
    print(p.greet())
    print(Person.from_birth_year("Asha", 2000).greet())
    print("Adult?", Person.is_adult(p.age))


# ---------------------------------------------------------------------------
# 2. ABSTRACT CLASS
# ---------------------------------------------------------------------------
class Shape(ABC):
    """Abstract base: defines the contract (area, perimeter) and shares `describe`."""

    def __init__(self, name: str):
        self.name = name  # shared state

    @abstractmethod
    def area(self) -> float:
        """Subclasses MUST implement this."""

    @abstractmethod
    def perimeter(self) -> float:
        """Subclasses MUST implement this."""

    def describe(self) -> str:
        # concrete method: reused by every subclass, built on the abstract ones
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius: float):
        super().__init__("Circle")
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


def demo_abstract_class():
    print("\n--- ABSTRACT CLASS ---")
    try:
        Shape("Generic")  # type: ignore[abstract]
    except TypeError as e:
        print("Cannot instantiate abstract class:", e)

    for shape in (Rectangle(3, 4), Circle(2)):
        print(shape.describe())  # polymorphism: same call, different behaviour


# ---------------------------------------------------------------------------
# 3. INTERFACE
# ---------------------------------------------------------------------------

# 3a) Interface via abstract class (nominal: must inherit explicitly)
class Flyable(ABC):
    @abstractmethod
    def fly(self) -> str: ...


class Swimmable(ABC):
    @abstractmethod
    def swim(self) -> str: ...


# A class can implement MULTIPLE interfaces (Python supports multiple inheritance)
class Duck(Flyable, Swimmable):
    def fly(self) -> str:
        return "Duck flaps wings and flies"

    def swim(self) -> str:
        return "Duck paddles on the water"


class Airplane(Flyable):  # unrelated to birds, but can still fly
    def fly(self) -> str:
        return "Airplane flies using engines"


# 3b) Interface via Protocol (structural: no inheritance required)
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...


class Square:  # note: does NOT inherit from Drawable
    def draw(self) -> str:
        return "Drawing a square"


class Text:
    def draw(self) -> str:
        return "Drawing some text"


def render(item: Drawable) -> None:
    # accepts anything that has a draw() method
    print(item.draw())


def demo_interface():
    print("\n--- INTERFACE (abstract-class style) ---")
    for thing in (Duck(), Airplane()):
        print(thing.fly())
    print(Duck().swim())

    print("\n--- INTERFACE (Protocol style) ---")
    for item in (Square(), Text()):
        render(item)
    print("Square is Drawable?", isinstance(Square(), Drawable))
    print("int is Drawable?", isinstance(5, Drawable))


if __name__ == "__main__":
    demo_class()
    demo_abstract_class()
    demo_interface()
