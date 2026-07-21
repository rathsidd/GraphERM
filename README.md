# GraphERM

**High-performance parallel engine for Euclidean Random Matrix (ERM) tracking on graphs.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21464997.svg)](https://doi.org/10.5281/zenodo.21464997)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

GraphERM computes multi-metric eigensystem criticality across an ensemble of
M = 1000 independent random matrix realizations per threshold step. It tracks
localized level-spacing contractions, wavefunction delocalization ratios, and
three distinct Shannon Information Entropies as a function of a geometric
distance threshold — revealing the critical connectivity at which a system
transitions from Anderson-localized to fully GOE-delocalized behavior.

Licensed under [GNU GPLv3](LICENSE).

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Reproducibility](#reproducibility)
- [Configuration](#configuration)
- [Output](#output)
- [Module Reference](#module-reference)
- [Scientific Background](#scientific-background)
- [Citation](#citation)

---

## Overview

GraphERM implements the **pyRMT-Sieve** algorithm:

1. A point cloud of `N` nodes is scattered in a `D`-dimensional box (1D, 2D,
   or 3D) using either a uniform random or periodic grid layout.
2. A full pairwise Euclidean distance matrix is computed for the point cloud.
3. For each of 15 evenly spaced distance thresholds `d`, a binary adjacency
   mask is constructed — connecting only node pairs within distance `d`.
4. `M = 1000` independent GOE (Gaussian Orthogonal Ensemble) matrices are
   generated in parallel, each element-wise masked by the adjacency matrix,
   then fully diagonalized.
5. Five metrics are tracked across all threshold steps and saved as
   publication-quality PNG plots.

The full parameter sweep runs across:
- **3 node counts:** 729, 4096, 15625
- **3 spatial dimensions:** 1D, 2D, 3D
- **2 coordinate regimes:** `uniform`, `grid`

producing **72 unique PNG output files** (4 panels × 3 nodes × 3 dims × 2 regimes).

---

## Repository Structure

```
GraphERM/
│
├── code/
│   ├── main.py        # Entry point — parameter loops and run orchestration
│   ├── config.py      # SpaceConfig — geometry and regime validation
│   ├── geometry.py    # CoordinateGenerator — point clouds and distance matrix
│   ├── entropy.py     # compute_shannon_entropy — normalized Shannon entropy
│   ├── ensemble.py    # GOE factory, parallel worker, MetricsSweepPipeline
│   └── plotting.py    # VisualEngineOrchestrator — isolated per-panel PNG export
│
├── requirements.txt
├── CITATION.cff
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

---

## Requirements

- Python 3.9+
- [NumPy](https://numpy.org/) >= 1.24
- [SciPy](https://scipy.org/) >= 1.11
- [Matplotlib](https://matplotlib.org/) >= 3.7

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/rathsidd/GraphERM.git
cd GraphERM
pip install -r requirements.txt
```

No additional package installation is required. The `code/` modules import
from each other using absolute path resolution via `sys.path`, so the entry
point works correctly regardless of where it is called from.

---

## Usage

### Run the full simulation (all 72 combinations)

From the **repo root**:

```bash
python code/main.py
```

From **inside** the `code/` directory:

```bash
cd code
python main.py
```

Both invocations are equivalent. The `sys.path` configuration in `main.py`
ensures local imports resolve correctly in either case.

### Run a single combination programmatically

```python
from code.main import run_simulation

run_simulation(n_nodes=729, dimensions=3, regime="uniform")
```

---

## Reproducibility

A fixed global random seed is set at the start of each simulation run to
ensure that all output figures are exactly reproducible across machines.
The seed is set in `run_simulation()` in `code/main.py` and can be changed
there if needed.

To reproduce the exact figures from the associated publication, run the
simulation with the default seed and default constants in `code/main.py`
without modification.

---

## Configuration

All top-level sweep parameters are declared as constants at the top of
`code/main.py` and can be edited directly:

| Constant | Default | Description |
|----------|---------|-------------|
| `NODE_COUNTS` | `[729, 4096, 15625]` | Node counts to sweep over |
| `DIMENSIONS` | `[1, 2, 3]` | Spatial dimensionalities to sweep over |
| `REGIMES` | `["uniform", "grid"]` | Coordinate layout modes |
| `M_REALIZATIONS` | `1000` | Number of GOE ensemble realizations per threshold step |
| `RANDOM_SEED` | `42` | Global NumPy random seed for reproducibility |

The threshold sweep window is **dynamically calibrated** at runtime from the
actual min/max pairwise distances of the generated point cloud, spanning from
`0.95 × d_min` to `0.45 × d_max` across 15 evenly spaced steps.

---

## Output

Each run produces 4 PNG files. With the default configuration, 72 PNG files
are written to the working directory.

### Filename pattern

```
panel_<X>_<label>_N<nodes>_<dim>D_<regime>.png
```

### Examples

```
panel_A_EMD_N729_3D_uniform.png
panel_B_EdgeSpacingStd_N4096_2D_grid.png
panel_C_EvecRatio_N15625_1D_uniform.png
panel_D_EntropyParadox_N729_3D_grid.png
```

### Panel descriptions

| Panel | Metric | Description |
|-------|--------|-------------|
| **A** | Earth Mover's Distance (EMD) | Wasserstein-1 distance between the pooled eigenvalue distribution and the theoretical GOE semicircle law |
| **B** | Edge Spacing Std Dev (σ_edge) | Standard deviation of eigenvalue gaps at the spectral edges across the ensemble — sensitive to localization transitions |
| **C** | Eigenvector L∞/L₂ Ratio | Mean and ±1σ error bands for edge and bulk eigenvector delocalization ratios across threshold steps |
| **D** | Entropy Paradox Fields | Three Shannon entropies plotted together: H_macro (global spectral envelope), H_micro (local level spacings), and H_ensemble (cross-ensemble boundary entropy) |

---

## Module Reference

### `config.py` — `SpaceConfig`
Validates and stores the spatial dimensionality, node count, and coordinate
regime for a given run. Raises `ValueError` on invalid inputs.

### `geometry.py` — `CoordinateGenerator`
Generates the node coordinate array (uniform random scatter or periodic grid)
and computes the full N×N pairwise Euclidean distance matrix.

### `entropy.py` — `compute_shannon_entropy`
Computes the normalized Shannon Information Entropy of a 1D data distribution
via histogram binning, with automatic zero-probability filtering.

### `ensemble.py` — `RandomEnsembleFactory`, `worker_process_realization`, `MetricsSweepPipeline`
- `RandomEnsembleFactory` — generates GOE matrices and the analytical
  semicircle reference eigenspectrum.
- `worker_process_realization` — top-level parallel worker function;
  diagonalizes one masked GOE realization and returns normalized eigenvalues,
  level spacings, and L∞/L₂ eigenvector ratios.
- `MetricsSweepPipeline` — orchestrates the `ProcessPoolExecutor` worker pool
  across all threshold steps and computes all five tracked metrics.

### `plotting.py` — `VisualEngineOrchestrator`
Generates and saves each of the four panels as a fully isolated Matplotlib
figure. Each figure is created, saved, and closed independently —
no axes or figure objects are shared between panels or across runs.

---

## Scientific Background

GraphERM is designed to locate the **critical geometric connectivity threshold**
at which a sparse random matrix ensemble transitions from:

- **Anderson-localized** behavior — eigenstates concentrated on isolated nodes,
  large spectral edge fluctuations, high L∞/L₂ ratios, EMD far from semicircle
- **GOE bulk universality** — extended (delocalized) eigenstates, rigid level
  repulsion, EMD converging to zero, entropies reaching stationary values

This transition is detected simultaneously across five metrics, with the
**Entropy Paradox** in Panel D — where H_macro and H_micro can move in
opposite directions — serving as a sensitive indicator of competing order and
disorder mechanisms near criticality.

The ensemble size M = 1000 is chosen for strict compliance with the
Law of Large Numbers, ensuring that all sample statistics (means, variances,
entropy estimates) are well-converged.

---

## Citation

If you use GraphERM in your research, please cite it using the metadata in
[CITATION.cff](CITATION.cff), or use the following BibTeX entry:

```bibtex
@software{grapherm,
  author  = {Siddharth S Rath},
  title   = {GraphERM: High-performance parallel engine for
             Euclidean Random Matrix tracking on graphs},
  year    = {2026},
  url     = {https://github.com/rathsidd/GraphERM},
  doi     = {10.5281/zenodo.21464997},
  license = {GPL-3.0}
}
```