# Verification

[Repository home](../README.md) · [Reproduce](reproducibility.md)

## Discrete structure

Let $D$ be the real Fourier differentiation matrix on an odd grid of $N=65$ points. It satisfies $D^T=-D$ to roundoff. Define

$$G=D\operatorname{diag}(A),\quad K=G^T\operatorname{diag}(m)G,\quad M=I+\varepsilon^2K.$$

For any real vector $v$,

$$v^TKv=(Gv)^T\operatorname{diag}(m)(Gv)\geq0.$$

The propagating initial surface is used as a test vector. Its absolute identity discrepancy is **1.92554 × 10⁻¹⁶**, below the asserted threshold $10^{-10}$. This is an algebraic check, not a statistical estimate.

The state $U=(Z,q)^T$ evolves under

$$\dot U=\begin{pmatrix}0&-D\\-M^{-1}D&0\end{pmatrix}U.$$

The implementation evaluates the action of the matrix exponential at the requested times. With $W=\operatorname{diag}(I,M)$, the block generator $\mathsf B$ satisfies $W\mathsf B+\mathsf B^TW=0$. Therefore

$$E_h=\frac{1}{2N}(Z^TZ+q^TMq)$$

is an exact invariant of the semidiscrete equations. Across the 80 standing-wave samples, the measured maximum $|E_h(t)/E_h(0)-1|$ is **3.33067 × 10⁻¹⁵**, below $10^{-10}$. The figure displays energy divided by its initial value.

## Reference spectral matrix

The nonzero Fourier coefficients of $H$ are

$$\widehat H_{0,0}=1,\quad \widehat H_{0,\pm1}=-0.25,\quad \widehat H_{\pm1,\pm1}=-0.05.$$

For row $(k,n)$ and column $(\ell,j)$, integration by parts gives

$$L_{(k,n),(\ell,j)}=\left[k\ell+\left(\frac{2\pi}{\varepsilon}\right)^2nj\right]\widehat H_{k-\ell,n-j}.$$

The generator constructs this matrix directly. At $\varepsilon=0.4$, changing the common Fourier cutoff from 12 to 14 changes the six retained squared frequencies by at most **1.79057 × 10⁻¹¹**, below the asserted threshold $10^{-8}$. The complete-model orders across successive scale halvings must exceed 3.8; all three do.

These are targeted checks for the distributed demonstration. They are not a complete grid-refinement study at every scale.

## Package checks

Run `tools/verify_showcase.py` as described in the reproduction guide. It checks:

- all local Markdown/HTML file references resolve;
- all ten GIFs contain multiple frames and match the inventory;
- no prohibited manuscript, CSV, archive, or compiled file type appears;
- stored numerical diagnostics satisfy the documented thresholds;
- required citation, permission, and documentation files exist.

The package checker validates stored outputs. To recompute those outputs, run the generator first. Small last-digit changes between numerical environments are expected.
