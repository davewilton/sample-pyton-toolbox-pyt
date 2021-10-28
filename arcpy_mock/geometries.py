"""
Objects for arcpy mocking
"""


class Geometry:
    """
    Base mock for arcgis poly objects
    """
    # pylint: disable=C0103,R0913
    def __init__(self, points, *args, **kwargs):
        if points.count == 0:
            raise RuntimeError("Object: CreateObject cannot create geometry from inputs")
        self._points = points._points  # pylint: disable=protected-access
        self._parts = [points]
        self.partCount = len(self._parts)

    def __iter__(self):
        return iter(self._parts)

    @property
    def pointCount(self):
        """
        Number of points in geometry

        :return: length of stored points list
        """
        return len(self._points)

    @property
    def firstPoint(self):
        """
        First point in geometry

        :return: First point in geometry
        """
        return self._points[0]

    @property
    def lastPoint(self):
        """
        Last point in geometry

        :return: Last point in geometry
        """
        return self._points[-1]

    def getPart(self, x):
        """get a part of a geometry"""
        return self._parts[x]

    def distanceTo(self, other):
        return 0

    def projectAs(self, a, b):
        # for mocks
        return self


class Multipoint(Geometry):
    type = 'multipoint'

    def __len__(self):
        return len(self._points)

    # noinspection PyPep8Naming,PyUnusedLocal
    def projectAs(self, spatial_reference, transformation_name=None):
        """Fixed project-as output for tests"""
        return [Point(1, -1, pt.Z) for pt in self._points]


class Polyline(Geometry):
    """
    Mock for an arcpy Polyline
    """
    type = "polyline"
    length = 1


class Polygon(Geometry):
    """
    Mock for an arcpy Polygon
    """
    type = "polygon"

    def intersect(self, other, dimension):
        return other

    # non zero for tests
    area = 99


class Point(Geometry):
    """
    Mock for an arcpy point
    """
    type = "point"
    data = []

    def __init__(self, X=0.0, Y=0.0, Z=None, M=None, ID=0):
        self.X, self.Y, self.Z, self.M, self.ID = X, Y, Z, M, ID
        self.data = []
        self.data.append(self)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    def __repr__(self):
        return '<Point ({}, {}, {}, {})>'.format(
            self.X,
            self.Y,
            self.Z if self.Z is not None else '#',
            self.M if self.M is not None else '#'
        )

    def __iter__(self):
        return iter(self)
