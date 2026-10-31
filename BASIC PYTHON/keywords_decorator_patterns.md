# Python Keywords, Decorators & Patterns

Every code block below is self-contained and runnable.

## Contents

1. [Keywords](#1-keywords)
2. [How decorators work](#2-how-decorators-work)
3. [Built-in decorators for classes](#3-built-in-decorators-for-classes)
4. [Standard-library decorators](#4-standard-library-decorators)
5. [Design patterns in Python](#5-design-patterns-in-python)
6. [Cheat sheet](#6-cheat-sheet)

---

## 1. Keywords

A **keyword** is a reserved word. You cannot use it as a variable name. Python 3.14 has 35 of them:

```python
import keyword

print(keyword.kwlist)       # hard keywords, always reserved
print(keyword.softkwlist)   # ['_', 'case', 'match', 'type'], reserved only in some contexts
```

`self`, `cls`, `super`, `print`, `len`, `property` are **not** keywords. `self` and `cls` are only naming conventions, and the rest are built-in names.

### Keywords grouped by job

| Group | Keywords |
|---|---|
| Values | `True` `False` `None` |
| Logic | `and` `or` `not` `is` `in` |
| Branching | `if` `elif` `else` `match` `case` |
| Loops | `for` `while` `break` `continue` |
| Functions | `def` `return` `lambda` `yield` |
| Classes | `class` |
| Errors | `try` `except` `finally` `raise` `assert` |
| Scope | `global` `nonlocal` `del` |
| Modules | `import` `from` `as` |
| Context | `with` |
| Async | `async` `await` |
| Placeholder | `pass` |

### Keywords that matter inside classes

```python
class Account:                                  # class: defines a class
    bank = "ABC"

    def __init__(self, owner, balance=0):       # def: defines a method
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:               # if / not / and / or
            raise ValueError("Insufficient")    # raise: throw an exception
        self.balance -= amount
        return self.balance                     # return: send a value back

    def history(self):
        yield "opened"                          # yield: makes this a generator
        yield f"balance={self.balance}"

    def __eq__(self, other):
        return isinstance(other, Account) and self.owner == other.owner

    def close(self):
        pass                                    # pass: do nothing (empty body)


a = Account("Asha", 100)
print(a.withdraw(30))                           # 70
print(list(a.history()))                        # ['opened', 'balance=70']
print(a is a, a == Account("Asha"))             # True True
print(None is None, "Asha" in ["Asha", "Ravi"]) # True True

try:
    a.withdraw(1000)
except ValueError as e:                         # try / except ... as
    print("Error:", e)
finally:
    print("always runs")                        # finally: runs no matter what
```

### `is` vs `==`

```python
a = [1, 2]
b = [1, 2]
print(a == b)    # True,  same value
print(a is b)    # False, different objects in memory
print(a is a)    # True,  same object
# Use `is` only for None/True/False: `if x is None`
```

### `global` and `nonlocal`

```python
count = 0

def inc_global():
    global count          # modify a module-level variable
    count += 1

def outer():
    n = 0
    def inner():
        nonlocal n        # modify the enclosing function's variable
        n += 1
        return n
    return inner

inc_global()
print(count)              # 1
f = outer()
print(f(), f(), f())      # 1 2 3
```

`nonlocal` is what makes closures and decorators with state possible.

### `with` (context managers)

```python
class Timer:
    def __enter__(self):
        print("start")
        return self
    def __exit__(self, exc_type, exc, tb):
        print("end")      # runs even if the body raised
        return False      # False = don't swallow the exception

with Timer() as t:
    print("working")
# start / working / end
```

### `lambda`, `assert`, `del`

```python
square = lambda x: x * x                 # tiny anonymous function
print(square(4))                         # 16

assert square(3) == 9, "math is broken"  # raises AssertionError if False

data = {"a": 1, "b": 2}
del data["a"]                            # remove a key/variable
print(data)                              # {'b': 2}
```

### `match` / `case` (soft keywords)

```python
def handle(cmd):
    match cmd:
        case "start":
            return "starting"
        case ["move", x, y]:
            return f"moving to {x},{y}"
        case {"type": "quit"}:
            return "bye"
        case _:
            return "unknown"

print(handle("start"), handle(["move", 1, 2]), handle({"type": "quit"}), handle(5))
```

### `async` / `await`

```python
import asyncio

async def fetch(n):
    await asyncio.sleep(0.01)    # pause here, let other tasks run
    return n * 2

async def main():
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results)               # [2, 4, 6]

asyncio.run(main())
```

---

## 2. How decorators work

A decorator is a function that takes a function and returns a (usually wrapped) function.
In Python, functions are objects, so you can pass them around and return them.

```python
@decorator
def f(): ...

# is exactly the same as:
def f(): ...
f = decorator(f)
```

### Step 1: a basic decorator

```python
def shout(func):
    def wrapper(*args, **kwargs):          # accept any arguments
        result = func(*args, **kwargs)     # call the original
        return result.upper()              # change the result
    return wrapper

@shout
def greet(name):
    return f"hello {name}"

print(greet("asha"))     # HELLO ASHA
```

### Step 2: always use `functools.wraps`

Without it, the wrapped function loses its name and docstring.

```python
from functools import wraps

def log_calls(func):
    @wraps(func)                           # keeps func.__name__ and __doc__
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

add(2, 3)
print(add.__name__, "|", add.__doc__)     # add | Add two numbers.
```

### Step 3: decorator with arguments (3 levels)

```python
from functools import wraps

def repeat(times):                         # level 1: takes the arguments
    def decorator(func):                   # level 2: takes the function
        @wraps(func)
        def wrapper(*args, **kwargs):      # level 3: the replacement
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)                                 # repeat(3) returns decorator, which wraps hello
def hello():
    print("hi")

hello()    # hi hi hi
```

### Step 4: stacking decorators (bottom runs first)

```python
def bold(f):
    return lambda *a, **k: f"<b>{f(*a, **k)}</b>"

def italic(f):
    return lambda *a, **k: f"<i>{f(*a, **k)}</i>"

@bold
@italic            # applied first, then bold wraps the result
def text():
    return "hi"

print(text())      # <b><i>hi</i></b>
```

### Step 5: a decorator that keeps state

```python
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def ping():
    return "pong"

ping(); ping()
print(ping.calls)    # 2
```

### Step 6: class-based decorator

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
    def __call__(self, *args, **kwargs):   # makes the instance callable
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    return "hi"

hello(); hello()
print(hello.calls)    # 2
```

### Step 7: decorating a class

A class decorator takes a class and returns a class.

```python
def add_repr(cls):
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{cls.__name__}({fields})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class User:
    def __init__(self, name, age):
        self.name, self.age = name, age

print(User("Asha", 30))    # User(name='Asha', age=30)
```

### Step 8: decorating methods (`self` is just the first argument)

```python
from functools import wraps

def require_admin(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_admin:
            raise PermissionError(f"{self.name} is not an admin")
        return method(self, *args, **kwargs)
    return wrapper

class User:
    def __init__(self, name, is_admin):
        self.name, self.is_admin = name, is_admin

    @require_admin
    def delete_all(self):
        return "deleted"

print(User("root", True).delete_all())
try:
    User("guest", False).delete_all()
except PermissionError as e:
    print("Error:", e)
```

### Common real-world decorators

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def retry(times=3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"attempt {attempt} failed: {e}")
                    if attempt == times:
                        raise
        return wrapper
    return decorator

attempts = {"n": 0}

@timer
@retry(times=3, exceptions=(ConnectionError,))
def flaky():
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise ConnectionError("network down")
    return "ok"

print(flaky())
```

---

## 3. Built-in decorators for classes

These need no import (except `abstractmethod`, which lives in `abc`).

### `@property`: method accessed like an attribute

```python
class Circle:
    def __init__(self, r):
        self._r = r

    @property
    def radius(self):                  # getter: c.radius
        return self._r

    @radius.setter
    def radius(self, value):           # setter: c.radius = 5
        if value <= 0:
            raise ValueError("radius must be positive")
        self._r = value

    @radius.deleter
    def radius(self):                  # deleter: del c.radius
        print("deleting radius")
        del self._r

    @property
    def area(self):                    # read-only: no setter defined
        return 3.14159 * self._r ** 2

c = Circle(2)
print(c.radius, round(c.area, 2))      # 2 12.57
c.radius = 5
try:
    c.radius = -1
except ValueError as e:
    print("Error:", e)
try:
    c.area = 10
except AttributeError as e:
    print("Error:", e)                 # read-only
del c.radius
```

### `@staticmethod`: no `self`, no `cls`

```python
class Temperature:
    @staticmethod
    def c_to_f(c):
        return c * 9 / 5 + 32

print(Temperature.c_to_f(100))         # 212.0
print(Temperature().c_to_f(0))         # 32.0, also works on an instance
```

### `@classmethod`: receives the class (`cls`)

```python
class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    @classmethod
    def margherita(cls):               # alternative constructor
        return cls(["cheese", "tomato"])

    @classmethod
    def from_string(cls, s):
        return cls(s.split(","))

class SpicyPizza(Pizza):
    pass

print(Pizza.margherita().toppings)
p = SpicyPizza.from_string("chili,cheese")
print(type(p).__name__, p.toppings)    # SpicyPizza ['chili', 'cheese']  (cls follows the subclass)
```

### `@abstractmethod` (from `abc`): subclass must implement

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...

    @property
    @abstractmethod                    # abstract property: order is @property on top
    def name(self): ...

    def receipt(self, amount):         # normal method, inherited as-is
        return f"{self.name}: paid {self.pay(amount)}"

class UPI(Payment):
    name = "UPI"
    def pay(self, amount):
        return amount

print(UPI().receipt(500))              # UPI: paid 500

try:
    Payment()
except TypeError as e:
    print("Error:", e)

class Broken(Payment):                 # forgot to implement pay and name
    pass

try:
    Broken()
except TypeError as e:
    print("Error:", e)
```

### Comparing the three method types

```python
class Demo:
    count = 0

    def instance_method(self):         # needs an object
        return f"instance {self}"

    @classmethod
    def class_method(cls):             # needs the class
        return f"class {cls.__name__}, count={cls.count}"

    @staticmethod
    def static_method(x):              # needs neither
        return x * 2

d = Demo()
print(d.instance_method() is not None)
print(Demo.class_method())
print(Demo.static_method(4))
```

---

## 4. Standard-library decorators

These need an import but are used with classes all the time.

### `@dataclass` (from `dataclasses`)

Generates `__init__`, `__repr__`, `__eq__` (and more) from annotated fields.

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: int
    y: int = 0                             # default value

print(Point(1, 2), Point(1) == Point(1, 0))   # Point(x=1, y=2) True

@dataclass(frozen=True, order=True)        # frozen: immutable and hashable, order: <, > work
class Version:
    major: int
    minor: int

v1, v2 = Version(1, 2), Version(1, 10)
print(v1 < v2)                             # True
try:
    v1.major = 5
except Exception as e:
    print("Error:", type(e).__name__)      # FrozenInstanceError

@dataclass
class Cart:
    owner: str
    items: list = field(default_factory=list)   # NEVER use items: list = []
    total: float = field(init=False, default=0)

    def __post_init__(self):               # runs right after the generated __init__
        self.owner = self.owner.title()

    def add(self, name, price):
        self.items.append(name)
        self.total += price

c = Cart("asha")
c.add("pen", 10)
print(c)    # Cart(owner='Asha', items=['pen'], total=10)
```

Useful options: `frozen=True`, `order=True`, `slots=True`, `kw_only=True`, `eq=False`.

### `@cached_property` (from `functools`)

Computed on first access, then stored on the instance.

```python
from functools import cached_property

class Report:
    @cached_property
    def data(self):
        print("(expensive load)")
        return [1, 2, 3]

r = Report()
print(r.data)    # prints (expensive load), then [1, 2, 3]
print(r.data)    # [1, 2, 3] only, served from cache
```

### `@total_ordering` (from `functools`)

Define `__eq__` plus one of `<`, `<=`, `>`, `>=`, and you get the rest.

```python
from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __eq__(self, other):
        return self.amount == other.amount
    def __lt__(self, other):
        return self.amount < other.amount

print(Money(5) < Money(9), Money(5) >= Money(9), Money(5) <= Money(5))
# True False True
```

### `@lru_cache` / `@cache` (from `functools`): memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))               # instant, would take forever without the cache
print(fib.cache_info())      # hits, misses, size
```

Do not put `@lru_cache` on instance methods without thinking: the cache keeps the instances alive.

### `@singledispatchmethod` (from `functools`): overload by argument type

```python
from functools import singledispatchmethod

class Formatter:
    @singledispatchmethod
    def fmt(self, value):
        return f"other: {value}"

    @fmt.register
    def _(self, value: int):
        return f"int: {value:,}"

    @fmt.register
    def _(self, value: list):
        return f"list of {len(value)}"

f = Formatter()
print(f.fmt(1000000), f.fmt([1, 2]), f.fmt("x"))
# int: 1,000,000 list of 2 other: x
```

### `@final` and `@override` (from `typing`)

Hints for type checkers like mypy and pyright. `@override` also sets `__override__` at runtime.

```python
from typing import final, override

class Base:
    @final
    def locked(self):                  # subclasses must not override this
        return "fixed"

    def greet(self):
        return "base"

class Child(Base):
    @override                          # checker errors if Base has no greet()
    def greet(self):
        return "child"

print(Child().greet(), Child().locked())
```

### `@overload` (from `typing`)

```python
from typing import overload

class Box:
    @overload
    def get(self, key: int) -> int: ...
    @overload
    def get(self, key: str) -> str: ...
    def get(self, key):                # the one real implementation
        return key

print(Box().get(1), Box().get("a"))
```

### `@unique` (from `enum`)

```python
from enum import Enum, unique

@unique                                # error if two members share a value
class Color(Enum):
    RED = 1
    GREEN = 2

print(Color.RED, Color(2).name)
```

### `@contextmanager` (from `contextlib`)

Write a `with` block using a generator instead of a class.

```python
from contextlib import contextmanager

@contextmanager
def opened(name):
    print(f"open {name}")
    try:
        yield name                     # the with-body runs here
    finally:
        print(f"close {name}")

with opened("db") as db:
    print("using", db)
```

### `@wraps` (from `functools`)

Already covered in section 2. Use it in every decorator you write.

### Where the built-ins come from

| Decorator | Import | Applies to |
|---|---|---|
| `@property` `@staticmethod` `@classmethod` | built-in | methods |
| `@abstractmethod` | `abc` | methods |
| `@dataclass` | `dataclasses` | classes |
| `@cached_property` `@total_ordering` `@lru_cache` `@cache` `@singledispatchmethod` `@wraps` | `functools` | methods / classes / functions |
| `@final` `@override` `@overload` | `typing` | methods / classes |
| `@unique` | `enum` | classes |
| `@contextmanager` | `contextlib` | functions |

---

## 5. Design patterns in Python

Python's features (first-class functions, decorators, duck typing) make many patterns shorter than in Java or C++.

### Singleton: one instance only

```python
class Config:
    _instance = None

    def __new__(cls):                  # __new__ creates the object, __init__ only sets it up
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

print(Config() is Config())            # True
```

As a reusable decorator:

```python
from functools import wraps

def singleton(cls):
    instances = {}
    @wraps(cls)
    def get(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get

@singleton
class Database:
    def __init__(self):
        print("connecting...")

print(Database() is Database())        # connecting... printed once, then True
```

### Factory: create objects without naming the class

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, msg): ...

class Email(Notifier):
    def send(self, msg): return f"email: {msg}"

class SMS(Notifier):
    def send(self, msg): return f"sms: {msg}"

class NotifierFactory:
    _types = {"email": Email, "sms": SMS}

    @classmethod
    def create(cls, kind) -> Notifier:
        try:
            return cls._types[kind]()
        except KeyError:
            raise ValueError(f"unknown notifier: {kind}")

print(NotifierFactory.create("sms").send("hi"))
```

### Registry via decorator: factory without editing the factory

```python
REGISTRY = {}

def register(name):
    def decorator(cls):
        REGISTRY[name] = cls
        return cls                     # return the class unchanged
    return decorator

@register("csv")
class CsvParser:
    def parse(self, s): return s.split(",")

@register("pipe")
class PipeParser:
    def parse(self, s): return s.split("|")

print(REGISTRY["pipe"]().parse("a|b|c"))    # ['a', 'b', 'c']
```

Adding a new parser means writing a new class only. Nothing else changes.

### Strategy: swap behavior at runtime

```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply(self, price): ...

class NoDiscount(Discount):
    def apply(self, price): return price

class Festive(Discount):
    def apply(self, price): return price * 0.8

class Cart:
    def __init__(self, strategy: Discount):
        self.strategy = strategy       # has-a (composition)
    def total(self, price):
        return self.strategy.apply(price)

cart = Cart(NoDiscount())
print(cart.total(100))                 # 100
cart.strategy = Festive()
print(cart.total(100))                 # 80.0
```

In Python a plain function often replaces the whole class hierarchy:

```python
def festive(price): return price * 0.8
def none(price): return price

class Cart:
    def __init__(self, discount): self.discount = discount
    def total(self, price): return self.discount(price)

print(Cart(festive).total(100))        # 80.0
```

### Observer: notify subscribers of events

```python
class EventBus:
    def __init__(self):
        self._subs = {}

    def subscribe(self, event, handler):
        self._subs.setdefault(event, []).append(handler)

    def publish(self, event, data):
        for handler in self._subs.get(event, []):
            handler(data)

bus = EventBus()
bus.subscribe("order", lambda d: print("email:", d))
bus.subscribe("order", lambda d: print("stock:", d))
bus.publish("order", {"id": 7})
```

### Template Method: fixed steps, customizable parts

```python
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    def run(self):                     # the template: order is fixed
        data = self.load()
        data = self.transform(data)
        return self.save(data)

    @abstractmethod
    def load(self): ...
    @abstractmethod
    def transform(self, data): ...
    def save(self, data):              # optional hook with a default
        return f"saved {data}"

class Doubler(DataPipeline):
    def load(self): return [1, 2, 3]
    def transform(self, data): return [x * 2 for x in data]

print(Doubler().run())                 # saved [2, 4, 6]
```

### Decorator pattern (wrapping objects, not the `@` syntax)

```python
class Coffee:
    def cost(self): return 50

class Milk:
    def __init__(self, inner): self.inner = inner
    def cost(self): return self.inner.cost() + 10

class Sugar:
    def __init__(self, inner): self.inner = inner
    def cost(self): return self.inner.cost() + 5

print(Sugar(Milk(Coffee())).cost())    # 65
```

### Builder: build a complex object step by step

```python
class Query:
    def __init__(self):
        self._table, self._where, self._limit = None, [], None

    def table(self, t):  self._table = t;           return self   # return self = chaining
    def where(self, c):  self._where.append(c);     return self
    def limit(self, n):  self._limit = n;           return self

    def build(self):
        sql = f"SELECT * FROM {self._table}"
        if self._where:
            sql += " WHERE " + " AND ".join(self._where)
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql

print(Query().table("users").where("age > 18").where("active = 1").limit(5).build())
```

### Iterator: make an object work in `for`

```python
class Countdown:
    def __init__(self, start):
        self.start = start
    def __iter__(self):                # generator = easiest iterator
        n = self.start
        while n > 0:
            yield n
            n -= 1

print(list(Countdown(3)))              # [3, 2, 1]
```

### Context manager: guaranteed setup and cleanup

```python
class Transaction:
    def __enter__(self):
        print("BEGIN")
        return self
    def __exit__(self, exc_type, exc, tb):
        print("ROLLBACK" if exc_type else "COMMIT")
        return False

with Transaction():
    print("work")                      # BEGIN / work / COMMIT

try:
    with Transaction():
        raise RuntimeError("boom")     # BEGIN / ROLLBACK
except RuntimeError:
    pass
```

### Descriptor: the machinery behind `@property`

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name)
    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError("must be positive")
        setattr(obj, self.name, value)

class Product:
    price = Positive()                 # reusable validation
    qty = Positive()
    def __init__(self, price, qty):
        self.price, self.qty = price, qty

p = Product(10, 2)
print(p.price, p.qty)
try:
    p.price = -5
except ValueError as e:
    print("Error:", e)
```

---

## 6. Cheat sheet

| I want to... | Use |
|---|---|
| Read a method like an attribute | `@property` |
| Validate on assignment | `@x.setter` |
| Force subclasses to implement a method | `@abstractmethod` + `ABC` |
| Build an object another way | `@classmethod` |
| Put a helper in the class with no `self` | `@staticmethod` |
| Compute once, then cache | `@cached_property` |
| Cache function results | `@lru_cache` / `@cache` |
| Skip writing `__init__`/`__repr__`/`__eq__` | `@dataclass` |
| Get all comparisons from one or two | `@total_ordering` |
| Stop subclasses overriding / catch typos | `@final` / `@override` |
| Write a `with` block as a function | `@contextmanager` |
| Wrap any function (log, time, retry, auth) | your own decorator + `@wraps` |
| Exactly one instance | Singleton (`__new__` or decorator) |
| Create objects by name | Factory / Registry |
| Swap algorithms at runtime | Strategy (class or plain function) |
| Notify many listeners | Observer |
| Fixed algorithm, custom steps | Template Method |

### Decorator template to copy

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper
```
