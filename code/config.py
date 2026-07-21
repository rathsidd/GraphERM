"""
SpaceConfig: structural parameters for geometric coordinate spaces.
"""


class SpaceConfig:
    """Encapsulates structural parameters for geometric coordinate spaces."""

    def __init__(self, dimensions: int, node_count: int, regime: str):
        """Initialize space configurations."""
        self.dimensions = dimensions
        self.node_count = node_count
        self.regime = regime.lower()
        self.validate_bounds()

    def validate_bounds(self):
        """Enforce strict geometric operational limits."""
        if self.dimensions not in {1, 2, 3}:
            raise ValueError("Dimensions must be 1, 2, or 3.")
        if self.regime not in {"grid", "uniform"}:
            raise ValueError("Regime must be 'grid' or 'uniform'.")