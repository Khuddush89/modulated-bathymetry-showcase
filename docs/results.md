# Computed results

[Repository home](../README.md) · [Mathematics](mathematical_overview.md)

All numerical values below were computed specifically for this package. Full precision is retained in [showcase_metrics.json](../results/showcase_metrics.json).

## Setup

| Quantity | Value |
| :-- | :-- |
| Longitudinal interval | $x\in[0,2\pi)$, periodic |
| Transverse cell | $Y\in[0,1)$, periodic |
| Amplitude | $A(x)=0.5+0.2\cos x$ |
| Effective flow scale | $\varepsilon=0.35$ |
| Flow grid | 65 equally spaced points |
| Displayed time | $0\leq t\leq2\pi$, 80 samples |
| Propagating initial data | $Z(x,0)=q(x,0)=0.2\cos x+0.1\sin2x$ |
| Standing initial data | $Z(x,0)=0.2\cos x+0.06\cos2x$, $q(x,0)=0$ |

The propagating initial data are used in the hero and wave-comparison figures. They are not an exact one-way eigenmode of the variable-coefficient effective model. The standing initial data are used for the phase/energy figure.

## Spectral comparison

For the full linear reference, use the positive operator

$$\mathcal L_\varepsilon=-\partial_x(H\partial_x)-\varepsilon^{-2}\partial_Y(H\partial_Y).$$

Its Fourier basis is $e^{ikx}e^{2\pi inY}$ with $|k|,|n|\leq12$. This gives a $625\times625$ Hermitian matrix. Its eigenvalues are squared frequencies. The effective reference is the generalized eigenproblem $-q_{xx}=\omega^2(I+\varepsilon^2\mathcal K_A)q$, discretized on the 65-point grid.

In each model, discard the constant zero mode, sort increasingly, and retain the first six squared frequencies. Define the reported error as the maximum absolute difference between the two sorted lists. Closely spaced pairs are compared by sorted position, without matching eigenvectors.

| ε | Complete operator error | Geometry-omitted error | Complete order |
| :-- | --: | --: | --: |
| 0.8 | 7.470792e-03 | 9.009337e-03 | n/a |
| 0.4 | 4.944655e-04 | 8.854587e-04 | 3.917 |
| 0.2 | 3.130217e-05 | 1.294608e-04 | 3.982 |
| 0.1 | 1.962488e-06 | 2.652782e-05 | 3.996 |


The observed order is $p=\log_2(e(\varepsilon)/e(\varepsilon/2))$. A fourth-order trend is resolved for the complete operator. The last omitted-term order is about 2.29; four points do not establish a universal asymptotic rate for that comparison.

## Dynamic comparisons

The complete model uses the factored $\mathcal K_A$. The nondispersive model sets $\mathcal K=0$. The geometry-omitted model retains only $-\partial_x(\mu\partial_x)$. All three use the same initial data and fixed $\varepsilon=0.35$.

In the wave figure, the upper panel plots the complete and nondispersive surfaces. The lower panel plots complete minus comparison, multiplied by $10^3$. This magnification exposes small differences without implying that either comparison is the exact physical solution.

## Interpretation and limits

The figures illustrate coefficient dependence, linear dispersive evolution, and an energy-preserving semidiscrete structure. The energy calculation is a property of the chosen discretization and does not by itself measure continuum accuracy. The spectral cutoff check is performed at one scale value. No experiment here validates nonlinear evolution, laboratory measurements, wave breaking, or a long-time approximation theorem.
