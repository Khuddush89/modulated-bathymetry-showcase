# Mathematical overview

[Repository home](../README.md) · [Results](results.md) · [Verification](verification.md)

This note derives the coefficient and identities used by the original showcase computations. Variables are nondimensional. The propagation coordinate is $x\in[0,2\pi)$, the transverse cell coordinate is $Y\in[0,1)$, and both are periodic.

## 1. Geometry and averages

Write

$$H(x,Y)=1-A(x)\beta(Y),\qquad \beta(Y)=\cos(2\pi Y).$$

The cell average is $\langle f\rangle_Y=\int_0^1 f(Y)\,dY$. Since $\langle\beta\rangle_Y=0$, we have $\langle H\rangle_Y=1$. The assumption $|A(x)|<1$ ensures positive depth. The flow examples use $A(x)=0.5+0.2\cos x$, so $0.3\leq A\leq0.7$ and $H\geq0.3$.

## 2. Exact cosine-cell coefficient

The mean-zero periodic primitive of $\beta$ is

$$B(Y)=\frac{\sin(2\pi Y)}{2\pi},\qquad B_Y=\beta.$$

Define

$$m(A)=\left\langle\frac{B^2}{H}\right\rangle_Y
=\frac1{4\pi^2}\frac1{2\pi}\int_0^{2\pi}\frac{\sin^2\theta}{1-A\cos\theta}\,d\theta.$$

For $A\ne0$, set $c=\cos\theta$. Polynomial division gives

$$\frac{1-c^2}{1-Ac}=\frac{c}{A}+\frac1{A^2}
+\frac{1-A^{-2}}{1-Ac}.$$

To evaluate the remaining average, split the integral at $\theta=\pi$ and use $u=\tan(\theta/2)$. Then

$$\int_0^{2\pi}\frac{d\theta}{1-A\cos\theta}
=2\int_{-\infty}^{\infty}\frac{du}{(1-A)+(1+A)u^2}
=\frac{2\pi}{\sqrt{1-A^2}}.$$

The average of $c$ vanishes. Thus

$$\frac1{2\pi}\int_0^{2\pi}\frac{\sin^2\theta}{1-A\cos\theta}\,d\theta
=\frac{1-\sqrt{1-A^2}}{A^2}
=\frac1{1+\sqrt{1-A^2}},$$

and therefore

$$\boxed{m(A)=\frac1{4\pi^2(1+\sqrt{1-A^2})}}.$$

The expression extends continuously to $m(0)=1/(8\pi^2)$. It is positive for $|A|<1$. The coefficient $\mu(A)=A^2m(A)$ can also be written as

$$\mu(A)=\frac{1-\sqrt{1-A^2}}{4\pi^2}.$$

For $0<A<1$, $\mu'(A)=A/(4\pi^2\sqrt{1-A^2})>0$. The coefficient animation displays this monotone dependence. Its moving amplitude is a parameter sweep, not an evolving bottom.

## 3. Factored correction and its expansion

For smooth periodic $w$, define

$$\mathcal K_Aw=-A\partial_x[m(A)\partial_x(Aw)].$$

With $m=m(A(x))$ and $\mu=A^2m$, expansion yields

$$\begin{aligned}
\mathcal K_Aw
&=-A\partial_x(mA w_x+mA'w)\\
&=-A^2m w_{xx}-[A(mA)_x+AmA']w_x-A(mA')_xw\\
&=-\partial_x(\mu w_x)-A(mA')_xw.
\end{aligned}$$

The geometry-omitted comparison uses $\mathcal K_{\rm omit}w=-\partial_x(\mu w_x)$. It is a different operator. The omitted multiplication term need not have one sign, although the complete factored operator is nonnegative as a quadratic form.

Indeed, periodic integration by parts gives

$$\int_0^{2\pi}v\mathcal K_Aw\,dx
=\int_0^{2\pi}m(A)\,\partial_x(Av)\,\partial_x(Aw)\,dx.$$

This proves symmetry. Taking $v=w$ proves nonnegativity. Consequently $I+\varepsilon^2\mathcal K_A$ has a coercive quadratic form for real $\varepsilon$.

## 4. Linear dynamics and energy

The animated solutions satisfy

$$Z_t=-q_x,\qquad Mq_t=-Z_x,\qquad M=I+\varepsilon^2\mathcal K_A.$$

For coefficients independent of time, define the spatially averaged energy

$$E=\frac1{4\pi}\int_0^{2\pi}[Z^2+q^2+\varepsilon^2m(A)((Aq)_x)^2],dx.$$

Using symmetry of $M$,

$$\frac{dE}{dt}=\frac1{2\pi}\int_0^{2\pi}(ZZ_t+qMq_t)\,dx
=-\frac1{2\pi}\int_0^{2\pi}(Zq_x+qZ_x)\,dx=0.$$

The final integral is a periodic boundary term. No time discretization is needed for this identity.

For a constant amplitude $A_0$, the Fourier mode with longitudinal wavenumber $k$ satisfies

$$\omega^2=\frac{k^2}{1+\varepsilon^2\mu(A_0)k^2}.$$

At $\varepsilon^2\mu k^2\ll1$, expansion gives $\omega^2=k^2-\varepsilon^2\mu k^4+O(\varepsilon^4k^6)$. This is a constant-coefficient calculation, not a dispersion relation for general variable $A(x)$.

## 5. Relation to weak nonlinearity

A formal weakly nonlinear extension adds $\alpha(Zq)_x$ to the mass equation and $\alpha q q_x$ to the momentum equation, with $\alpha=\varepsilon^2$. Those terms are **not** included in the animations or spectral calculations. The conserved quadratic energy derived above applies to the linear system. This showcase supplies neither a nonlinear homogenization proof nor a uniform long-time error estimate.
