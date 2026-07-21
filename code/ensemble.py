"""
ensemble: GOE matrix factory, parallel worker, and sweep pipeline.
"""

import concurrent.futures

import numpy as np
import scipy.stats as stats

from config import SpaceConfig
from entropy import compute_shannon_entropy


class RandomEnsembleFactory:
    """Generates pure, dense Gaussian Orthogonal Ensembles (the laser)."""

    @staticmethod
    def generate_goe_base(matrix_dim: int) -> np.ndarray:
        """Generate a single GOE matrix of given dimension."""
        mat = np.random.normal(0.0, 1.0, (matrix_dim, matrix_dim))
        return (mat + mat.T) / np.sqrt(2.0 * matrix_dim)

    @staticmethod
    def generate_analytical_semicircle(sample_size: int) -> np.ndarray:
        """Generate eigenvalues of a GOE matrix as a semicircle reference."""
        mat = np.random.normal(0.0, 1.0, (sample_size, sample_size))
        mat = (mat + mat.T) / np.sqrt(2.0 * sample_size)
        return np.linalg.eigvalsh(mat)


def worker_process_realization(adj_mask: np.ndarray, n: int):
    """Parallel worker: diagonalizes a single matrix realization H_j."""
    goe_base = RandomEnsembleFactory.generate_goe_base(n)
    h_eff = adj_mask * goe_base

    # Complete eigensystem decomposition
    evals, evecs = np.linalg.eigh(h_eff)

    # Globally normalize spectrum boundaries between [-2, 2] centered at 0
    lambda_min, lambda_max = evals[0], evals[-1]
    if lambda_max != lambda_min:
        normalized_evals = (
            4.0 * ((evals - lambda_min) / (lambda_max - lambda_min)) - 2.0
        )
    else:
        normalized_evals = evals

    raw_spacings = np.diff(normalized_evals)
    linf_l2_ratios = np.max(np.abs(evecs), axis=0)

    return normalized_evals, raw_spacings, linf_l2_ratios


class MetricsSweepPipeline:
    """Orchestrates parallelized multi-metric entropy sweeps via workers."""

    def __init__(
        self,
        config: SpaceConfig,
        thresholds: np.ndarray,
        dist_matrix: np.ndarray,
        ensemble_size: int = 1000,
    ):
        """Initialize pipeline parameters with hard-locked geometry."""
        self.config = config
        self.thresholds = thresholds
        self.ensemble_size = ensemble_size
        self.dist_matrix = dist_matrix
        self.reference_semicircle = (
            RandomEnsembleFactory.generate_analytical_semicircle(500)
        )

    def evaluate_sweep(self):
        """Run the multi-core parameter sweep across all threshold steps."""
        emd_profile = []
        edge_spacing_std_profile = []

        # Entropy tracker profiles
        h_macro_profile = []
        h_micro_profile = []
        h_ensemble_edge_profile = []

        # Wavefunction tracker profiles
        edge_evec_mean_profile = []
        edge_evec_std_profile = []
        bulk_evec_mean_profile = []
        bulk_evec_std_profile = []

        n = self.config.node_count

        for d in self.thresholds:
            adj_mask = (self.dist_matrix <= d).astype(float)

            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(worker_process_realization, adj_mask, n)
                    for _ in range(self.ensemble_size)
                ]

                evals_list = []
                spacing_ensemble_block = np.zeros((self.ensemble_size, n - 1))
                evec_ratio_ensemble_block = np.zeros((self.ensemble_size, n))

                for idx, future in enumerate(
                    concurrent.futures.as_completed(futures)
                ):
                    ev, sp, vec_r = future.result()
                    evals_list.append(ev)
                    spacing_ensemble_block[idx, :] = sp
                    evec_ratio_ensemble_block[idx, :] = vec_r

            # -----------------------------------------------------------------
            # LAYER 1: Global Macro Scale Tracking
            # -----------------------------------------------------------------
            pooled_normalized_evals = np.concatenate(evals_list)
            emd = stats.wasserstein_distance(
                pooled_normalized_evals, self.reference_semicircle
            )
            emd_profile.append(emd)

            # Entropy 1: Global Envelope Shannon Entropy H_macro
            h_macro_profile.append(
                compute_shannon_entropy(pooled_normalized_evals, bins=60)
            )

            # -----------------------------------------------------------------
            # LAYER 2: Local Eigenvalue Fluctuations Tracking
            # -----------------------------------------------------------------
            spacing_index_std = np.std(spacing_ensemble_block, axis=0)
            edge_spacing_indices = [0, 1, n - 3, n - 2]
            edge_spacing_std_profile.append(
                np.mean(spacing_index_std[edge_spacing_indices])
            )

            # Entropy 2: Local Spacing Shannon Entropy H_micro
            pooled_spacings = spacing_ensemble_block.flatten()
            h_micro_profile.append(
                compute_shannon_entropy(pooled_spacings, bins=60)
            )

            # -----------------------------------------------------------------
            # LAYER 3: Wavefunction Delocalization & Ensemble Entropy Tracking
            # -----------------------------------------------------------------
            evec_index_mean = np.mean(evec_ratio_ensemble_block, axis=0)
            evec_index_std = np.std(evec_ratio_ensemble_block, axis=0)

            edge_cutoff = int(n * 0.15)
            edge_vec_indices = np.concatenate(
                [np.arange(edge_cutoff), np.arange(n - edge_cutoff, n)]
            )
            bulk_vec_indices = np.arange(edge_cutoff, n - edge_cutoff)

            edge_evec_mean_profile.append(
                np.mean(evec_index_mean[edge_vec_indices])
            )
            edge_evec_std_profile.append(
                np.mean(evec_index_std[edge_vec_indices])
            )
            bulk_evec_mean_profile.append(
                np.mean(evec_index_mean[bulk_vec_indices])
            )
            bulk_evec_std_profile.append(
                np.mean(evec_index_std[bulk_vec_indices])
            )

            # Entropy 3: Cross-Ensemble Index-Isolated Boundary Entropy
            edge_vector_universe_population = evec_ratio_ensemble_block[:, 0]
            h_ensemble_edge_profile.append(
                compute_shannon_entropy(
                    edge_vector_universe_population, bins=40
                )
            )

        return (
            np.array(emd_profile),
            np.array(edge_spacing_std_profile),
            np.array(h_macro_profile),
            np.array(h_micro_profile),
            np.array(h_ensemble_edge_profile),
            np.array(edge_evec_mean_profile),
            np.array(edge_evec_std_profile),
            np.array(bulk_evec_mean_profile),
            np.array(bulk_evec_std_profile),
        )