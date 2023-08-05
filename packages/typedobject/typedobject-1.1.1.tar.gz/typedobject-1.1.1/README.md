# typedobject

Define real, inheritable, and efficient Python classes using `TypedDict`-like
syntax.

## Getting started

Install from pip.

    python -m pip install typedobject

Then, annotate your class with `typedobject` and declare its member fields
using variable annotations.

    from typedobject import typedobject

    @typedobject
    class Point:
        x: int
        y: int

Then construct the object using either positional or keyword arguments.

    pt1 = Point(10, 20)
    pt2 = Point(x=10, y=20)
    assert pt1 == pt2

You can define methods, including `__init__`.

    @typedobject
    class Rectangle:
        pt1: Point
        pt2: Point

        def __init__(self, x1, y1, x2, y2):
            self.pt1 = Point(x1, y1)
            self.pt2 = Point(x2, y2)

        def area(self):
            return (self.pt2.x - self.pt1.x) * (self.pt2.y - self.pt1.y)

    rect = Rectangle(1, 1, 3, 3)
    assert rect.area() == 4

Unlike `TypedDict`, the defined classes are actually fresh new classes,
not `dict`s.

    assert isinstance(rect, Rectangle)
    assert not isinstance(rect, Point)

Inheritance works just fine.

    @typedobject
    class RoundedRect(Rectangle):
        corner_radius: int

    rr = RoundedRect(Point(1, 1), Point(3, 3), 1)

Note that the derived class overrides `__init__`, unless you use `.no_init`.

    @typedobject.no_init
    class RoundedRect2(Rectangle):
        corner_radius: int

    rr = RoundedRect2(1, 1, 3, 3)
    assert not hasattr(rr, 'corner_radius')

Typed object classes, unlike `dataclass`, specify `__slots__`, which makes
access to attributes faster and makes objects take less memory, but prevents
adding new fields dynamically.

They also prevent multiple inheritance.

    # raises TypeError
    class RectangleWithAPoint(Rectangle, Point):
        pass

You can, however, inject mixins.

    class TwoDObjectMixin:
        def area(self):
            return self.width() * self.height()

    @typedobject
    class Rectangle2(TwoDObjectMixin):
        pt1: Point
        pt2: Point
