import pytest

def test_readme():
    # pylint: disable=unused-variable
    # pylint: disable=no-value-for-parameter

    from typedobject import typedobject

    @typedobject
    class Point:
        x: int
        y: int

    pt1 = Point(10, 20)
    pt2 = Point(x=10, y=20)
    assert pt1 == pt2

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

    assert isinstance(rect, Rectangle)
    assert not isinstance(rect, Point)

    @typedobject
    class RoundedRect(Rectangle):
        corner_radius: int

    rr = RoundedRect(Point(1, 1), Point(3, 3), 1)

    @typedobject.no_init
    class RoundedRect2(Rectangle):
        corner_radius: int

    rr = RoundedRect2(1, 1, 3, 3)
    assert not hasattr(rr, 'corner_radius')

    with pytest.raises(TypeError):
        class RectangleWithAPoint(Rectangle, Point):
            pass

    class TwoDObjectMixin:
        def area(self):
            return self.width() * self.height()

    @typedobject
    class Rectangle2(TwoDObjectMixin):
        pt1: Point
        pt2: Point
