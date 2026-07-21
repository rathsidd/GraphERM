# Contributing to GraphERM

Thank you for your interest in contributing to GraphERM.
This document outlines the guidelines for contributing code,
reporting issues, and suggesting improvements.

---

## Reporting Issues

If you encounter a bug or unexpected behaviour, please open a
[GitHub Issue](https://github.com/rathsidd/GraphERM/issues) and include:

- A minimal reproducible example
- Your Python version (`python --version`)
- Your package versions (`pip freeze`)
- The full error traceback if applicable

---

## Suggesting Enhancements

Feature requests and scientific extensions are welcome. Please open an issue
describing:

- The proposed change and its scientific motivation
- Any relevant references or prior work

---

## Contributing Code

### 1. Fork and clone the repository

```bash
git clone https://github.com/<your-username>/GraphERM.git
cd GraphERM
```

### 2. Install dependencies

```bash
pip install numpy scipy matplotlib
```

### 3. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Follow the existing code style

- All code must be **PEP 8 compliant**
- Every function, method, and class must have a **docstring**
- No hardcoded parameters — declare constants explicitly at the module level
- New modules must follow the single-responsibility structure of the existing
  `code/` layout

### 5. Test your changes

There is currently no automated test suite. Before submitting, manually
verify that:

- `python code/main.py` runs without errors
- Output PNG files are generated with correct filenames
- No existing module interfaces are broken

### 6. Open a Pull Request

Push your branch and open a pull request against `main`. Include a clear
description of what was changed and why.

---

## Code of Conduct

Please be respectful and constructive in all interactions.
This project follows the
[Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).