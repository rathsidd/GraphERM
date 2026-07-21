"""
CoordinateGenerator: coordinate tensor generation and pairwise distances.
"""

import numpy as np

from config import SpaceConfig


class CoordinateGenerator:
    """Generates coordinate tensors and metric distance transformations."""

    @staticmethod
    def generate_coordinates(
        config: SpaceConfig, box_length: float = 10.0
    ) -> np.ndarray:
        """Generate node coordinates based on the space configuration."""
        if config.regime == "uniform":
            return np.random.uniform(
                0.0, box_length, (config.node_count, config.dimensions)
            )

        if config.dimensions == 1:
            return np.linspace(
                0.0, box_length, config.node_count
            ).reshape(-1, 1)

        if config.dimensions == 2:
            pts_per_axis = int(np.ceil(np.sqrt(config.node_count)))
            axis = np.linspace(0.0, box_length, pts_per_axis)
            x, y = np.meshgrid(axis, axis)
            return np.vstack([x.ravel(), y.ravel()]).T[: config.node_count]

        if config.dimensions == 3:
            pts_per_axis = int(np.ceil(np.cbrt(config.node_count)))
            axis = np.linspace(0.0, box_length, pts_per_axis)
            x, y, z = np.meshgrid(axis, axis, axis)
            return np.vstack(
                [x.ravel(), y.ravel(), z.ravel()]
            ).T[: config.node_count]

        return np.zeros((config.node_count, config.dimensions))

    @staticmethod
    def compute_pairwise_distances(coords: np.ndarray) -> np.ndarray:
        """Compute the full pairwise Euclidean distance matrix."""
        return np.sqrt(
            np.sum(
                (coords[:, None, :] - coords[None, :, :]) ** 2, axis=-1
            )
        )