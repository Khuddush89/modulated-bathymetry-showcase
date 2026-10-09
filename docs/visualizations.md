# Figure guide

[Repository home](../README.md) · [Static gallery](static_gallery.md)

The fixed navy panels make all figures readable on either GitHub page theme. Motion is supplied by local GIFs; no script, embed, remote image service, or browser extension is required. Navigation cards are links and mathematical notes use native expandable details. The figures themselves are not draggable or parameter-controlled.

| Asset | Meaning | Playback |
| :-- | :-- | :-- |
| [Research header](../assets/header/research-wave.gif) | Averaged surface $Z$ above the stationary depth map $H(x,Y)$ | Actual linear evolution on $[0,2\pi]$, then restart |
| [Cell coefficient](../assets/animations/cell-coefficient.gif) | The cell depth and $\mu(A)$ as prescribed amplitude varies | Smooth parameter sweep from 0.075 to 0.9 and back |
| [Wave comparison](../assets/animations/wave-comparison.gif) | Complete vs nondispersive surface, with magnified differences from two comparisons | Actual linear evolution, then restart |
| [Phase and energy](../assets/animations/phase-energy.gif) | Fixed-probe $(Z,q)$ trace and global energy components | Standing-data evolution, then restart |
| [Spectral convergence](../assets/animations/spectral-convergence.gif) | Four computed errors and an $\varepsilon^4$ reference slope | Progressive reveal, not a continuous parameter simulation |
| [Overview tile](../assets/section_headers/overview.gif) | Changing cosine-cell depth | Miniature coefficient sweep |
| [Framework tile](../assets/section_headers/framework.gif) | Moving point on $\mu(A)$ | Parameter sweep |
| [Results tile](../assets/section_headers/results.gif) | Miniature averaged surface | Samples from the computed flow |
| [Verification tile](../assets/section_headers/verification.gif) | Surface and velocity/cell energy fractions | Samples from the standing-data calculation |
| [Wave divider](../assets/section_headers/wave-divider.gif) | A normalized sinusoidal travelling mode | Phase advances by $2\pi$ per loop |

## Reading the header

The depth image is a map of the fixed function $1-(0.5+0.2\cos x)\cos(2\pi Y)$. Horizontal position is $x\in[0,2\pi]$; vertical position is $Y\in[0,1]$. Dark to light indicates smaller to greater depth over the range 0.3 to 1.7. The gold line scans at $x=t$ modulo $2\pi$ to connect the two panels. It is a guide, not a moving bottom, tracked crest, or fluid particle.

## Reading the phase plot

The probe is grid index 11, at $x_*=22\pi/65\approx1.063$. Horizontal position is $Z(x_*,t)$ and vertical position is $q(x_*,t)$. The dim curve shows the whole displayed interval; the coloured trace reveals the interval already elapsed. It need not close exactly. The bars show surface energy, combined velocity/cell energy, and total energy, each divided by the initial total.

## Reading the spectral animation

The horizontal and vertical axes are logarithmic. Cyan is the complete operator and gold is the geometry-omitted comparison. The dark slope guide is normalized to the first complete-model error and is proportional to $\varepsilon^4$. An order is shown only after a second scale value is available. Animation frames between stages hold the same computed values; no uncomputed spectral samples are implied.

## Playback and accessibility

Time-dependent solutions replay a finite interval, so the final-to-first reset is intentional. The coefficient sweeps and sinusoidal divider are cyclic. Playback speed is chosen for viewing and differs from model time. GIF delays are quantized to hundredths of a second, and identical frames may be merged by the encoder. All graphs have static alternatives and text explanations. To avoid motion, open the static gallery directly instead of the animated README.
