import argparse

def get_config():
    """
    Parses command-line arguments for the Boid simulation.

    Returns:
        argparse.Namespace: A namespace containing all configuration parameters.
    """
    parser = argparse.ArgumentParser(description="Boid Simulation Configuration")

    # Screen parameters
    parser.add_argument("--screen-width", dest="screen_width", type=int, default=800, help="Width of the simulation window")
    parser.add_argument("--screen-height", dest="screen_height", type=int, default=600, help="Height of the simulation window")

    # Boid parameters
    parser.add_argument("--num-boids", dest="num_boids", type=int, default=50, help="Number of Boids in the simulation")
    parser.add_argument("--boid-height", dest="boid_height", type=int, default=10, help="Boid's height (for rendering)")
    parser.add_argument("--boid-width", dest="boid_width", type=int, default=3, help="Boid's width (for rendering)")
    
    # Velocity parameters
    parser.add_argument("--max-velocity", dest="max_velocity", type=float, default=2.0, help="Maximum velocity magnitude for Boids")

    # Flocking behavior weights
    parser.add_argument("--separation-intensity", dest="separation_intensity", type=float, default=100, help="Intensity of separation force")
    parser.add_argument("--separation-weight", dest="separation_weight", type=float, default=1, help="Weight of separation behavior")
    parser.add_argument("--alignment-weight", dest="alignment_weight", type=float, default=0.03, help="Weight of alignment behavior")
    parser.add_argument("--cohesion-weight", dest="cohesion_weight", type=float, default=0.001, help="Weight of cohesion behavior")

    # Interaction radii
    parser.add_argument("--separation-radius", dest="separation_radius", type=float, default=60, help="Radius for separation force")
    parser.add_argument("--alignment-radius", dest="alignment_radius", type=float, default=80, help="Radius for alignment force")
    parser.add_argument("--cohesion-radius", dest="cohesion_radius", type=float, default=80, help="Radius for cohesion force")

    return parser.parse_args()


CONFIG = get_config()



# python main.py --num-boids 100 --width 1024 --height 768
