import pygame
import pygame.gfxdraw
from config import CONFIG
from boidmanager import BoidManager

# Pygame Configuration
screen = pygame.display.set_mode((CONFIG.screen_width, CONFIG.screen_height))
pygame.display.set_caption("Boid Simulation")


def run_simulation() -> None:
    """
    Runs the Boid simulation using Pygame.

    The simulation continuously updates the Boid positions and their interactions,
    applying flocking behavior rules (separation, alignment, cohesion) while using 
    a KD-Tree for efficient neighbor searches.
    """
    pygame.init()
    clock = pygame.time.Clock()
    is_running = True

    # Initialize the BoidManager with simulation parameters
    boid_manager = BoidManager(
        width=CONFIG.screen_width,
        height=CONFIG.screen_height,
        num_boids=CONFIG.num_boids,
        boid_height=CONFIG.boid_height,
        boid_width=CONFIG.boid_width,
        max_velocity=CONFIG.max_velocity,
        separation_intensity=CONFIG.separation_intensity,
        separation_weight=CONFIG.separation_weight,
        alignment_weight=CONFIG.alignment_weight,
        cohesion_weight=CONFIG.cohesion_weight
    )

    while is_running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # Black background

        # Event handling (Exit on window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        # Update KD-Tree for efficient neighbor queries
        boid_manager.update_kdtree()

        for boid in boid_manager.boids:
            # Retrieve different groups of neighbors for each flocking rule
            neighbors_separation = boid_manager.get_neighbors(boid, radius=CONFIG.separation_radius)
            neighbors_alignment = boid_manager.get_neighbors(boid, radius=CONFIG.alignment_radius)
            neighbors_cohesion = boid_manager.get_neighbors(boid, radius=CONFIG.cohesion_radius)

            # Update Boid movement based on flocking rules
            boid.update(neighbors_separation, neighbors_alignment, neighbors_cohesion)
            boid_manager.apply_screen_wrap(boid)

            # Render Boid with anti-aliased edges
            pygame.gfxdraw.aapolygon(screen, boid.vertices, boid.color)
            pygame.gfxdraw.filled_polygon(screen, boid.vertices, boid.color)

        pygame.display.flip()

    pygame.quit()
