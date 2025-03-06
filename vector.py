import numpy as np


class Vector:
    """A 2D vector class with basic vector operations."""

    def __init__(self, components: list | tuple | np.ndarray):
        """
        Initializes a Vector with two components.

        Args:
            components (list | tuple | np.ndarray): A sequence of two numeric values representing the vector.

        Raises:
            ValueError: If components is not a list, tuple, or np.ndarray of length 2.
        """
        if not isinstance(components, (list, tuple, np.ndarray)) or len(components) != 2:
            raise ValueError("components must be a list, tuple, or numpy array of length 2")
        
        self.components = np.array(components, dtype=float)

    def __repr__(self) -> str:
        """Returns a string representation of the vector."""
        return f"Vector({self.components[0]}, {self.components[1]})"

    def __add__(self, other: "Vector") -> "Vector":
        """
        Adds two vectors component-wise.

        Args:
            other (Vector): Another Vector instance.

        Returns:
            Vector: The resulting vector after addition.

        Raises:
            TypeError: If the operand is not an instance of Vector.
        """
        if not isinstance(other, Vector):
            raise TypeError("Operand must be an instance of Vector")
        return Vector(self.components + other.components)

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtracts one vector from another component-wise.

        Args:
            other (Vector): Another Vector instance.

        Returns:
            Vector: The resulting vector after subtraction.

        Raises:
            TypeError: If the operand is not an instance of Vector.
        """
        if not isinstance(other, Vector):
            raise TypeError("Operand must be an instance of Vector")
        return Vector(self.components - other.components)

    def __mul__(self, scalar: float) -> "Vector":
        """
        Multiplies a vector by a scalar.

        Args:
            scalar (float): The scalar value to multiply with.

        Returns:
            Vector: The resulting vector after scaling.

        Raises:
            TypeError: If the operand is not a float or integer.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Operand must be a scalar (int or float)")
        return Vector(self.components * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """
        Enables scalar multiplication from the left.

        Args:
            scalar (float): The scalar value.

        Returns:
            Vector: The resulting vector.
        """
        return self.__mul__(scalar)

    def dot(self, other: "Vector") -> float:
        """
        Computes the dot product between two vectors.

        Args:
            other (Vector): Another Vector instance.

        Returns:
            float: The dot product of the two vectors.

        Raises:
            TypeError: If the operand is not an instance of Vector.
        """
        if not isinstance(other, Vector):
            raise TypeError("Operand must be an instance of Vector")
        return np.dot(self.components, other.components)

    def magnitude(self) -> float:
        """
        Computes the magnitude (length) of the vector.

        Returns:
            float: The magnitude of the vector.
        """
        return np.linalg.norm(self.components)

    def normalize(self) -> "Vector":
        """
        Returns a normalized (unit length) version of the vector.

        Returns:
            Vector: A unit vector in the same direction.

        Raises:
            ValueError: If the vector has zero magnitude.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector(self.components / mag)

    def perpendicular(self) -> "Vector":
        """
        Returns a perpendicular vector rotated 90 degrees counterclockwise.

        Returns:
            Vector: The perpendicular vector.
        """
        return Vector([-self.components[1], self.components[0]])
