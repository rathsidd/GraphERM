"""
main: entry point — runs the full sweep for all node counts, dimensions,
and regimes, then saves all panel PNGs.

Produces 4 panels x 3 node counts x 3 dimensions x 2 regimes
= 72 unique PNG files.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from config import SpaceConfig
from geometry import CoordinateGenerator
from ensemble import MetricsSweepPipeline
from plotting import VisualEngineOrchestrator

NODE_COUNTS = [729, 4096, 15625]
DIMENSIONS = [1, 2, 3]
REGIMES = ["uniform", "grid"]
M_REALIZATIONS = 1000  # Strict compliance with the Law of Large Numbers
RANDOM_SEED = 42

def run_simulation(n_nodes: int, dimensions: int, regime: str) -> None:
    """Run the full sweep pipeline for one (n_nodes, dimensions, regime) case.

    Args:
        n_nodes: Number of nodes in the point cloud.
        dimensions: Spatial dimensionality (1, 2, or 3).
        regime: Coordinate layout — 'uniform' or 'grid'.
    """
    print(
        f"\n{'=' * 60}\n"
        f"Launching Field Engine  "
        f"(N={n_nodes}, M={M_REALIZATIONS}, "
        f"D={dimensions}, Regime={regime})...\n"
        f"{'=' * 60}"
    )
    
    np.random.seed(RANDOM_SEED)
    config = SpaceConfig(
        dimensions=dimensions, node_count=n_nodes, regime=regime
    )
    coords = CoordinateGenerator.generate_coordinates(
        config, box_length=10.0
    )
    dist_matrix = CoordinateGenerator.compute_pairwise_distances(coords)

    # Dynamic Geometric Radius Calibration (The Adaptive Sieve)
    non_zero_distances = dist_matrix[dist_matrix > 0]
    sweep_start = np.min(non_zero_distances) * 0.95
    sweep_end = np.max(dist_matrix) * 0.45
    threshold_sweep = np.linspace(sweep_start, sweep_end, 15)

    print(
        f"Calibrated Sweep Window: "
        f"[{round(sweep_start, 3)} -> {round(sweep_end, 3)}]"
    )
    print("Spawning Multi-Core Process Worker Pools Across CPU Cores...")

    pipeline = MetricsSweepPipeline(
        config, threshold_sweep, dist_matrix, ensemble_size=M_REALIZATIONS
    )
    results = pipeline.evaluate_sweep()

    print(
        f"Sweep complete. Saving panels for "
        f"N={n_nodes}, D={dimensions}, Regime={regime}..."
    )
    VisualEngineOrchestrator.save_all_panels(
        threshold_sweep, results, n_nodes, M_REALIZATIONS, dimensions, regime
    )
    print(
        f"All panels saved for N={n_nodes}, D={dimensions}, "
        f"Regime={regime}.\n"
    )


if __name__ == "__main__":
    # Standard multi-processing loop guard for Python process forks.
    for n in NODE_COUNTS:
        for d in DIMENSIONS:
            for regime in REGIMES:
                run_simulation(n, d, regime)