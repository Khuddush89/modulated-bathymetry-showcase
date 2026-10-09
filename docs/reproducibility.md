# Reproduction guide

[Repository home](../README.md) · [Verification](verification.md)

The repository already contains all finished figures. Rebuilding is optional. The original generator computes its own trajectories and spectra, then draws each asset. It does not download images, source files, or datasets.

## Environment

The delivered outputs were generated with Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and Pillow 12.3.0. These tools are dependencies, not distributed repository contents. Install them from their standard distribution channels. Use an installed DejaVu Sans font, including its bold face, for the supplied typography. No font file is bundled. The generator first tries the standard Linux font directory and then installed font names; adjust `FONT_DIR` if needed on another system.

## Rebuild

From the extracted repository directory, create an isolated environment if desired, then run:

```sh
python -m pip install -r requirements.txt
python tools/build_showcase.py
python tools/verify_showcase.py
```

The generator replaces the generated files in `assets/` and `results/`. It evaluates several dense spectral problems and encodes ten GIFs. Runtime depends on the machine and numerical library configuration. Setting `OPENBLAS_NUM_THREADS=1` before execution can limit parallel library threads on systems that use OpenBLAS.

## What is deterministic?

There are no random inputs. Equations, initial data, palettes, frame times, and dimensions are explicit in the generator. The invariant and convergence thresholds should reproduce. Floating-point last digits, font rasterization, and GIF encoding can differ across platforms. Byte-identical files are not promised outside the recorded environment.

The results tables in the documentation describe the delivered run. If you change parameters, update the prose and tables to match the new JSON outputs.

## Acknowledgements

NumPy supplies array operations, SciPy supplies linear algebra and matrix-exponential actions, and Pillow supplies drawing and GIF encoding. DejaVu Sans provides installed typography. These independently maintained tools are acknowledged here; their code and font binaries are not included in this repository.
