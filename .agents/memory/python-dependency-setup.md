---
name: Python dependency setup
description: Replit dependency inference and installation quirks observed during setup.
---

Check inferred dependencies before accepting automatic Python package installation.
The installer can mistake local modules for unrelated third-party packages.

**Why:** During setup, inferred local module names pulled in an unrelated machine-learning dependency incompatible with Python 3.12.

**How to apply:** Compare inferred dependencies with actual imports and local modules; install only genuine external dependencies.

An installer failure does not prove required packages are unavailable.

**Why:** A later installation attempt tried to write into the read-only Nix Python directory, while the required packages were already importable from the project package directory.

**How to apply:** Check imports and versions before retrying or changing the runtime. Keep the dependency manifest accurate even when installation reports failure.
