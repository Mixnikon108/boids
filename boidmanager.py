from boid import Boid
from point import Point
from vector import Vector
import numpy as np
from scipy.spatial import KDTree
from typing import List


class BoidManager:
    """
    A class responsible for managing Boids and their interactions using KD-Tree 
    for efficient neighbor searches.

    The KD-Tree significantly improves the performance of nearest neighbor searches, 
    making it an ideal choice for real-time simulations with a large number of Boids.
    """

    def __init__(self, width: int, 
                 height: int, 
                 num_boids: int, 
                 boid_height: float, 
                 boid_width: float, 
                 max_velocity: float,
                 separation_intensity: float = 3.0,
                 separation_weight: float = 0.5,
                 alignment_weight: float = 0.03,
                 cohesion_weight: float = 0.001):
        """
        Initializes the BoidManager and sets up the flock and KD-Tree.

        Args:
            width (int): Width of the simulation space.
            height (int): Height of the simulation space.
            num_boids (int): Number of Boids in the simulation.
            boid_height (float): Height of each Boid (for rendering).
            boid_width (float): Width of each Boid (for rendering).
            max_velocity (float): Maximum velocity magnitude for Boids.
        """
        self.width = width
        self.height = height
        self.num_boids = num_boids
        self.boid_height = boid_height
        self.boid_width = boid_width
        self.max_velocity = max_velocity
        self.separation_intensity = separation_intensity
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.boids = self.initialize_boids()
        self.kd_tree = None  # KD-Tree will be updated each frame

    def initialize_boids(self) -> List[Boid]:
        """
        Creates a list of Boids with random positions and velocities.

        Returns:
            List[Boid]: A list of initialized Boid instances.
        """
        boids = []
        for _ in range(self.num_boids):
            position = Point([
                np.random.uniform(0, self.width), 
                np.random.uniform(0, self.height)
            ])
            velocity = Vector([
                np.random.uniform(-1, 1), 
                np.random.uniform(-1, 1)
            ]).normalize() * self.max_velocity  # Normalize to max velocity
            
            heading = np.arctan2(velocity.components[1], velocity.components[0])
            boids.append(Boid(self.boid_height, self.boid_width, position, heading, velocity, self.max_velocity,
                              self.separation_intensity, self.separation_weight, self.alignment_weight, self.cohesion_weight))
        return boids

    def update_kdtree(self) -> None:
        """
        Updates the KD-Tree with the current Boid positions.

        Why use KD-Tree?
        ----------------
        - A naive approach for finding nearest neighbors requires checking each Boid 
          against all others, which results in O(n²) complexity.
        - KD-Tree reduces this to **O(log n)** for queries, making neighbor searches 
          significantly faster in large-scale simulations.
        """
        positions = np.array([boid.position.coordinates for boid in self.boids])
        self.kd_tree = KDTree(positions)

    def get_neighbors(self, boid: Boid, radius: float) -> List[Boid]:
        """
        Retrieves neighboring Boids within a given radius using KD-Tree.

        Args:
            boid (Boid): The Boid for which we are finding neighbors.
            radius (float): The search radius.

        Returns:
            List[Boid]: A list of neighboring Boids within the radius.
        """
        if self.kd_tree is None:
            return []  # No KD-Tree available yet

        # Find indices of neighbors using KD-Tree query
        neighbor_indices = self.kd_tree.query_ball_point(boid.position.coordinates, radius)

        # Filter out the Boid itself from its neighbor list
        return [self.boids[i] for i in neighbor_indices if self.boids[i] != boid]

    def apply_screen_wrap(self, boid: Boid) -> None:
        """
        Implements toroidal (wrap-around) boundary conditions.

        If a Boid moves past one edge of the screen, it appears on the opposite side.

        Args:
            boid (Boid): The Boid to apply the wrapping logic to.
        """
        boid.position.coordinates = np.mod(boid.position.coordinates, [self.width, self.height])
