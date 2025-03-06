import numpy as np
from vector import Vector


class Point:
    """Represents a 2D point with basic vector operations."""

    def __init__(self, coordinates: list[float] | tuple[float, float] | np.ndarray):
        """
        Initializes a Point object.

        Args:
            coordinates (list, tuple, or np.ndarray): A 2-element iterable representing (x, y).
        
        Raises:
            ValueError: If the input is not a valid 2D point.
        """
        if not isinstance(coordinates, (list, tuple, np.ndarray)) or len(coordinates) != 2:
            raise ValueError("coordinates must be a list, tuple, or numpy array of length 2")
        self.coordinates = np.array(coordinates, dtype=float)

    def __repr__(self) -> str:
        """Returns a string representation of the Point object."""
        return f"Point({self.coordinates[0]}, {self.coordinates[1]})"

    def __add__(self, other: "Point") -> "Point":
        """
        Adds two Point objects component-wise.

        Args:
            other (Point): Another Point object.
        
        Returns:
            Point: A new Point representing the sum.
        
        Raises:
            TypeError: If the operand is not a Point instance.
        """
        if not isinstance(other, Point):
            raise TypeError("Operand must be an instance of Point")
        return Point(self.coordinates + other.coordinates)

    def __sub__(self, other: "Point") -> "Vector":
        """
        Subtracts two Point objects, returning a Vector.

        Args:
            other (Point): Another Point object.
        
        Returns:
            Vector: A new Vector representing the difference.
        
        Raises:
            TypeError: If the operand is not a Point instance.
        """
        if not isinstance(other, Point):
            raise TypeError("Operand must be an instance of Point")
        return Vector(self.coordinates - other.coordinates)

    def __mul__(self, scalar: float) -> "Point":
        """
        Multiplies the Point by a scalar.

        Args:
            scalar (float): A scalar value.
        
        Returns:
            Point: A new Point scaled by the scalar.
        
        Raises:
            TypeError: If the operand is not a float or int.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Operand must be a scalar (int or float)")
        return Point(self.coordinates * scalar)

    def __rmul__(self, scalar: float) -> "Point":
        """
        Supports scalar multiplication from both directions (scalar * Point).

        Args:
            scalar (float): A scalar value.
        
        Returns:
            Point: A new Point scaled by the scalar.
        """
        return self.__mul__(scalar)

    def as_tuple(self) -> tuple[float, float]:
        """
        Returns the coordinates of the Point as a tuple.

        Returns:
            tuple: A tuple (x, y) representing the Point's coordinates.
        """
        return tuple(self.coordinates)
