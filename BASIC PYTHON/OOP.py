"""
OOP in Python: classes, objects, and the four pillars.
Run: python3 OOP.py
"""
from abc import ABC, abstractmethod


# ---------------------------------------------------------------
# 1. CLASS & OBJECT
# A class is a blueprint; an object is an instance of it.
# ---------------------------------------------------------------
class Dog:
    species = "Canis familiaris"      # class attribute: shared by all dogs

    def __init__(self, name, age):    # constructor: runs on Dog(...)
        self.name = name              # instance attributes: per object
        self.age = age

    def speak(self):                  # method; `self` is the object itself
        return f"{self.name} says woof"

    def __str__(self):                # dunder: controls print(obj)
        return f"Dog({self.name}, {self.age})"


def demo_class():
    print("== 1. Class & Object ==")
    d1 = Dog("Rex", 3)
    d2 = Dog("Bella", 5)
    print(d1.speak())
    print(d2, "| species:", Dog.species)


# ---------------------------------------------------------------
# 2. ENCAPSULATION
# Bundle data with methods and protect it from invalid changes.
# `_name` = "private by convention"; `__name` = name-mangled.
# ---------------------------------------------------------------
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance       # not meant to be touched directly

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    @property                         # read-only access via account.balance
    def balance(self):
        return self._balance


def demo_encapsulation():
    print("\n== 2. Encapsulation ==")
    acc = BankAccount("Chirag", 100)
    acc.deposit(50)
    print("Balance:", acc.balance)
    try:
        acc.withdraw(1000)            # rules enforced by the class
    except ValueError as e:
        print("Error:", e)


# ---------------------------------------------------------------
# 3. ABSTRACTION
# Define WHAT must be done, hide HOW. An abstract class can't be
# instantiated; subclasses must implement the abstract methods.
# ---------------------------------------------------------------
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    def describe(self):               # concrete method shared by all shapes
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


def demo_abstraction():
    print("\n== 3. Abstraction ==")
    try:
        Shape()                       # not allowed
    except TypeError as e:
        print("Error:", e)
    print(Circle(2).describe())


# ---------------------------------------------------------------
# 4. INHERITANCE  ("is-a")
# A child class reuses and extends a parent; super() calls the parent.
# ---------------------------------------------------------------
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)        # reuse parent's constructor
        self.indoor = indoor

    def speak(self):                  # override parent's method
        return f"{self.name} says meow"


class Puppy(Dog):                     # multi-level: Puppy -> Dog
    def speak(self):
        return super().speak() + " (squeaky)"


def demo_inheritance():
    print("\n== 4. Inheritance ==")
    c = Cat("Tom")
    print(c.speak(), "| is Animal?", isinstance(c, Animal))
    print(Puppy("Max", 1).speak())


# ---------------------------------------------------------------
# 5. POLYMORPHISM
# Same method call, different behavior depending on the object.
# The caller doesn't care about the concrete type.
# ---------------------------------------------------------------
class Cow(Animal):
    def speak(self):
        return f"{self.name} says moo"


def demo_polymorphism():
    print("\n== 5. Polymorphism ==")
    zoo = [Animal("Generic"), Cat("Tom"), Cow("Daisy")]
    for a in zoo:
        print(a.speak())              # each class runs its own version

    # Duck typing: anything with .area() works, no shared parent needed
    shapes = [Circle(1), Rectangle(2, 3)]
    print("Total area:", sum(s.area() for s in shapes))


# ---------------------------------------------------------------
# 6. COMPOSITION ("has-a") - often better than inheritance
# Build objects out of other objects.
# ---------------------------------------------------------------
class Engine:
    def start(self):
        return "Engine started"


class Car:
    def __init__(self, engine):
        self.engine = engine          # Car HAS an Engine

    def start(self):
        return f"Car: {self.engine.start()}"


def demo_composition():
    print("\n== 6. Composition ==")
    print(Car(Engine()).start())


# ---------------------------------------------------------------
# 7. DUNDER METHODS: make objects work with built-in syntax
# ---------------------------------------------------------------
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):         # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):          # v1 == v2
        return self.x == other.x and self.y == other.y

    def __repr__(self):               # unambiguous debug string
        return f"Vector({self.x}, {self.y})"


def demo_dunder():
    print("\n== 7. Dunder methods ==")
    print(Vector(1, 2) + Vector(3, 4), "| equal?", Vector(1, 1) == Vector(1, 1))


if __name__ == "__main__":
    demo_class()
    demo_encapsulation()
    demo_abstraction()
    demo_inheritance()
    demo_polymorphism()
    demo_composition()
    demo_dunder()
