# Boid Flocking Simulation

![Boid Simulation](https://miro.medium.com/v2/resize:fit:720/format:webp/1*c9VTUIXfsfWXgsaIfbGV8Q.png)
*A visualization of the Boid flocking simulation.*

## Overview
This project is a **Boid flocking simulation** that models the collective movement of autonomous agents (Boids) in a 2D environment. The simulation implements **separation**, **alignment**, and **cohesion** behaviors to mimic real-world flocking, using **KD-Trees** for optimized nearest-neighbor searches.

For a deep dive into the mathematical and computational aspects of this simulation, check out my Medium article:
[Boids: Simulating Flocking Behavior with Mathematics and KD-Trees](https://medium.com/@jorgechedo/boids-simulating-flocking-behavior-with-mathematics-and-kd-trees-be61f8f787f4).

## Installation & Running
Ensure you have Python installed, along with the necessary dependencies:

```bash
pip install pygame numpy scipy
```

To start the simulation, simply run:

```bash
python main.py
```

You can customize simulation parameters by modifying `config.py` or providing command-line arguments:

```bash
python main.py --num-boids 100 --screen-width 1024 --screen-height 768
```

## Project Structure
```
boid_simulation/
│── boid.py           # Defines individual Boid behavior (separation, alignment, cohesion)
│── boidmanager.py    # Manages Boid interactions and KD-Tree optimization
│── config.py         # Configuration file for simulation parameters
│── main.py           # Entry point to run the simulation
│── point.py          # 2D point representation with vector operations
│── simulation.py     # Handles the main simulation loop and rendering
│── vector.py         # Vector class for 2D calculations
```

### Why Use KD-Trees?

In a naive approach, each Boid would check all other Boids to determine neighbors, leading to **O(n²) complexity**. For large simulations, this becomes impractical.

Using a **KD-Tree**, we efficiently structure Boid positions in a way that allows nearest-neighbor searches in **O(log n)** time. This optimization significantly improves performance, making real-time flocking simulations scalable.

The KD-Tree implementation is found in `boidmanager.py`, where it is used to efficiently query neighbors within a given radius.
