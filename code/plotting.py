"""
plotting: VisualEngineOrchestrator — per-panel figure saving.
"""

import matplotlib.pyplot as plt
import numpy as np


class VisualEngineOrchestrator:
    """Manages multi-axis Matplotlib panel generation and PNG export."""

    @staticmethod
    def _build_subtitle(
        n_nodes: int, m_realizations: int, dimensions: int, regime: str
    ) -> str:
        """Construct a shared figure subtitle string from run parameters."""
        return (
            f"N = {n_nodes}, M = {m_realizations} Ensembles "
            f"| {dimensions}D | Regime: {regime}"
        )

    @staticmethod
    def _build_filename(
        panel: str, label: str, n_nodes: int, dimensions: int, regime: str
    ) -> str:
        """Construct a unique PNG filename from run parameters.

        Pattern: panel_<X>_<label>_N<n>_<d>D_<regime>.png
        Example: panel_A_EMD_N729_3D_uniform.png
        """
        return f"panel_{panel}_{label}_N{n_nodes}_{dimensions}D_{regime}.png"

    @staticmethod
    def _plot_panel_a(
        threshold_sweep: np.ndarray,
        emd: np.ndarray,
        n_nodes: int,
        m_realizations: int,
        dimensions: int,
        regime: str,
    ) -> None:
        """Save Panel A: Global Macro-State Deformation Profile (EMD)."""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(
            threshold_sweep, emd, marker="o", color="purple",
            linewidth=2.5, label="EMD Path",
        )
        ax.set_title(
            "A. Global Macro-State Deformation Profile (Wasserstein-1)",
            fontsize=11, fontweight="bold",
        )
        ax.set_xlabel("Distance Parameter Threshold (d)", fontsize=10)
        ax.set_ylabel("Earth Mover's Distance", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        fig.suptitle(
            VisualEngineOrchestrator._build_subtitle(
                n_nodes, m_realizations, dimensions, regime
            ),
            fontsize=10, y=1.01,
        )
        fig.tight_layout()
        filename = VisualEngineOrchestrator._build_filename(
            "A", "EMD", n_nodes, dimensions, regime
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  Saved: {filename}")
        plt.close(fig)

    @staticmethod
    def _plot_panel_b(
        threshold_sweep: np.ndarray,
        edge_sp_std: np.ndarray,
        n_nodes: int,
        m_realizations: int,
        dimensions: int,
        regime: str,
    ) -> None:
        """Save Panel B: Local Eigenvalue Spacing Std Dev Profile."""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(
            threshold_sweep, edge_sp_std, marker="s", color="crimson",
            linewidth=2.5, label="Edge Spacings σ",
        )
        ax.set_title(
            "B. Local Eigenvalue Spacing Standard Deviation Profile",
            fontsize=11, fontweight="bold",
        )
        ax.set_xlabel("Distance Parameter Threshold (d)", fontsize=10)
        ax.set_ylabel("Index-Isolated Ensemble σ_edge", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        fig.suptitle(
            VisualEngineOrchestrator._build_subtitle(
                n_nodes, m_realizations, dimensions, regime
            ),
            fontsize=10, y=1.01,
        )
        fig.tight_layout()
        filename = VisualEngineOrchestrator._build_filename(
            "B", "EdgeSpacingStd", n_nodes, dimensions, regime
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  Saved: {filename}")
        plt.close(fig)

    @staticmethod
    def _plot_panel_c(
        threshold_sweep: np.ndarray,
        edge_v_mean: np.ndarray,
        edge_v_std: np.ndarray,
        bulk_v_mean: np.ndarray,
        bulk_v_std: np.ndarray,
        n_nodes: int,
        m_realizations: int,
        dimensions: int,
        regime: str,
    ) -> None:
        """Save Panel C: Eigenvector L_inf/L_2 Ratio Error-Band Profile."""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(
            threshold_sweep, edge_v_mean, color="navy",
            linewidth=2.5, label="Edge Vector Mean",
        )
        ax.fill_between(
            threshold_sweep, edge_v_mean - edge_v_std,
            edge_v_mean + edge_v_std, color="navy", alpha=0.15,
        )
        ax.plot(
            threshold_sweep, bulk_v_mean, color="darkorange",
            linewidth=2.0, linestyle="--", label="Bulk Vector Mean",
        )
        ax.fill_between(
            threshold_sweep, bulk_v_mean - bulk_v_std,
            bulk_v_mean + bulk_v_std, color="darkorange", alpha=0.1,
        )
        ax.set_title(
            "C. Eigenvector L_inf/L_2 Ratio Error-Band Profile",
            fontsize=11, fontweight="bold",
        )
        ax.set_xlabel("Distance Parameter Threshold (d)", fontsize=10)
        ax.set_ylabel("Index-Pooled Ratio Statistics", fontsize=10)
        ax.legend(loc="upper right")
        ax.grid(True, linestyle="--", alpha=0.5)
        fig.suptitle(
            VisualEngineOrchestrator._build_subtitle(
                n_nodes, m_realizations, dimensions, regime
            ),
            fontsize=10, y=1.01,
        )
        fig.tight_layout()
        filename = VisualEngineOrchestrator._build_filename(
            "C", "EvecRatio", n_nodes, dimensions, regime
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  Saved: {filename}")
        plt.close(fig)

    @staticmethod
    def _plot_panel_d(
        threshold_sweep: np.ndarray,
        h_macro: np.ndarray,
        h_micro: np.ndarray,
        h_ensemble: np.ndarray,
        n_nodes: int,
        m_realizations: int,
        dimensions: int,
        regime: str,
    ) -> None:
        """Save Panel D: Information-Theoretic Entropy Paradox Fields."""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax_twin = ax.twinx()
        (p1,) = ax.plot(
            threshold_sweep, h_macro, marker="^", color="teal",
            linewidth=2.0, label="Macro Envelope Entropy (H_macro)",
        )
        (p2,) = ax.plot(
            threshold_sweep, h_micro, marker="v", color="forestgreen",
            linewidth=2.0, linestyle="--",
            label="Local Spacing Entropy (H_micro)",
        )
        ax.set_ylabel(
            "H_macro & H_micro Shannon Scale", color="teal", fontsize=10
        )
        ax.tick_params(axis="y", labelcolor="teal")
        (p3,) = ax_twin.plot(
            threshold_sweep, h_ensemble, marker="d", color="darkviolet",
            linewidth=2.5,
            label="Cross-Ensemble Edge Entropy (H_ensemble)",
        )
        ax_twin.set_ylabel(
            "H_ensemble Boundary Scale", color="darkviolet", fontsize=10
        )
        ax_twin.tick_params(axis="y", labelcolor="darkviolet")
        lines = [p1, p2, p3]
        ax.legend(
            lines, [line.get_label() for line in lines],
            loc="lower left", fontsize=9,
        )
        ax.set_title(
            "D. The Information-Theoretic Entropy Paradox Fields",
            fontsize=11, fontweight="bold",
        )
        ax.set_xlabel("Distance Parameter Threshold (d)", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.3)
        fig.suptitle(
            VisualEngineOrchestrator._build_subtitle(
                n_nodes, m_realizations, dimensions, regime
            ),
            fontsize=10, y=1.01,
        )
        fig.tight_layout()
        filename = VisualEngineOrchestrator._build_filename(
            "D", "EntropyParadox", n_nodes, dimensions, regime
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"  Saved: {filename}")
        plt.close(fig)

    @staticmethod
    def save_all_panels(
        threshold_sweep: np.ndarray,
        results: tuple,
        n_nodes: int,
        m_realizations: int,
        dimensions: int,
        regime: str,
    ) -> None:
        """Save all four panels for a given run configuration.

        Args:
            threshold_sweep: Array of distance threshold values.
            results: Full tuple returned by MetricsSweepPipeline.evaluate_sweep.
            n_nodes: Number of nodes used in the simulation.
            m_realizations: Number of ensemble realizations.
            dimensions: Spatial dimensionality of the point cloud.
            regime: Coordinate layout — 'uniform' or 'grid'.
        """
        (
            emd, edge_sp_std,
            h_macro, h_micro, h_ensemble,
            edge_v_mean, edge_v_std,
            bulk_v_mean, bulk_v_std,
        ) = results

        VisualEngineOrchestrator._plot_panel_a(
            threshold_sweep, emd, n_nodes, m_realizations, dimensions, regime
        )
        VisualEngineOrchestrator._plot_panel_b(
            threshold_sweep, edge_sp_std,
            n_nodes, m_realizations, dimensions, regime
        )
        VisualEngineOrchestrator._plot_panel_c(
            threshold_sweep,
            edge_v_mean, edge_v_std, bulk_v_mean, bulk_v_std,
            n_nodes, m_realizations, dimensions, regime,
        )
        VisualEngineOrchestrator._plot_panel_d(
            threshold_sweep,
            h_macro, h_micro, h_ensemble,
            n_nodes, m_realizations, dimensions, regime,
        )