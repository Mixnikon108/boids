from point import Point
from vector import Vector
import numpy as np
from typing import List


class Boid:
    """A class representing a Boid in a flocking simulation."""

    def __init__(
        self,
        height: float,
        width: float,
        position: Point,
        heading: float,
        velocity: Vector = None,
        max_velocity: float = 2.0,
        separation_intensity: float = 3.0,
        separation_weight: float = 0.5,
        alignment_weight: float = 0.03,
        cohesion_weight: float = 0.001
    ):
        """
        Initializes a Boid with given properties.

        Args:
            height (float): Height of the Boid (used for rendering).
            width (float): Width of the Boid (used for rendering).
            position (Point): The Boid's position in 2D space.
            heading (float): The Boid's heading (angle in radians).
            velocity (Vector, optional): The Boid's initial velocity. Defaults to (0,0).
            max_velocity (float, optional): Maximum velocity magnitude. Defaults to 2.0.
            separation_intensity (float, optional): Strength of the separation force. Defaults to 3.0.
            separation_weight (float, optional): Weight of the separation behavior. Defaults to 0.5.
            alignment_weight (float, optional): Weight of the alignment behavior. Defaults to 0.03.
            cohesion_weight (float, optional): Weight of the cohesion behavior. Defaults to 0.001.
        """
        self.height = height
        self.width = width
        self.position = position
        self.heading = heading
        self.color = (255, 255, 255)  # White color for the Boid
        self.velocity = velocity if velocity is not None else Vector([0, 0])
        self.vertices = self._compute_vertices()
        self.max_velocity = max_velocity
        self.separation_intensity = separation_intensity
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight

    def _compute_vertices(self) -> List[tuple]:
        """
        Computes the vertices of the Boid's triangle shape.

        Returns:
            List[tuple]: A list of 3 tuples representing the triangle vertices.
        """
        return [
            (self.position + self.height * Point([np.cos(self.heading), np.sin(self.heading)])).as_tuple(),
            (self.position + self.width * Point([-np.sin(self.heading), np.cos(self.heading)])).as_tuple(),
            (self.position + self.width * Point([np.sin(self.heading), -np.cos(self.heading)])).as_tuple()
        ]

    def update(self, neighbors_separation: List["Boid"], neighbors_alignment: List["Boid"], neighbors_cohesion: List["Boid"]) -> None:
        """
        Updates the Boid's velocity and position based on the flocking rules.

        Args:
            neighbors_separation (List[Boid]): Boids used for separation.
            neighbors_alignment (List[Boid]): Boids used for alignment.
            neighbors_cohesion (List[Boid]): Boids used for cohesion.
        """
        separation_force = self.separation(neighbors_separation) * self.separation_weight
        alignment_force = self.alignment(neighbors_alignment) * self.alignment_weight
        cohesion_force = self.cohesion(neighbors_cohesion) * self.cohesion_weight

        # Update velocity based on the computed forces
        self.velocity = self.velocity + separation_force + alignment_force + cohesion_force

        # Limit the velocity to max_velocity
        self.velocity = self.velocity.normalize() * self.max_velocity

        # Update position and direction
        self.position = self.position + Point(self.velocity.components)
        self.heading = np.arctan2(self.velocity.components[1], self.velocity.components[0])
        self.vertices = self._compute_vertices()

    def separation(self, neighbors: List["Boid"]) -> Vector:
        """
        Computes the separation force to avoid collisions with nearby Boids.

        Args:
            neighbors (List[Boid]): Nearby Boids.

        Returns:
            Vector: The separation force.
        """
        separation_force = Vector([0, 0])

        for neighbor in neighbors:
            distance_vector = self.position - neighbor.position
            distance_magnitude = distance_vector.magnitude()
            repulsion = distance_vector.normalize() * (self.separation_intensity / distance_magnitude)
            separation_force = separation_force + repulsion

        # Average the force if there are neighbors
        if len(neighbors) > 0:
            separation_force = separation_force * (1 / len(neighbors))

        return separation_force

    def alignment(self, neighbors: List["Boid"]) -> Vector:
        """
        Computes the alignment force to steer towards the average velocity of neighbors.

        Args:
            neighbors (List[Boid]): Nearby Boids.

        Returns:
            Vector: The alignment force.
        """
        if len(neighbors) == 0:
            return Vector([0, 0])  # No alignment if no neighbors are present

        avg_velocity = sum((neighbor.velocity for neighbor in neighbors), Vector([0, 0])) * (1 / len(neighbors))
        alignment_force = avg_velocity - self.velocity  # Adjust towards the group's velocity

        return alignment_force

    def cohesion(self, neighbors: List["Boid"]) -> Vector:
        """
        Computes the cohesion force to move towards the center of mass of nearby Boids.

        Args:
            neighbors (List[Boid]): Nearby Boids.

        Returns:
            Vector: The cohesion force.
        """
        if len(neighbors) == 0:
            return Vector([0, 0])  # No cohesion if no neighbors are present

        avg_position = sum((neighbor.position for neighbor in neighbors), Point([0, 0])) * (1 / len(neighbors))
        cohesion_force = Vector(avg_position.coordinates - self.position.coordinates)  # Move towards the center

        return cohesion_force
