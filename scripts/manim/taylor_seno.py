from manim import *
import numpy as np
from math import factorial
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; GRIS = "#555555"

def P(n):
    return lambda x: sum((-1) ** k * x ** (2 * k + 1) / factorial(2 * k + 1) for k in range((n - 1) // 2 + 1))

class TaylorSeno(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-8, 8, 2], y_range=[-2.5, 2.5, 1], x_length=12, y_length=5.2,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                    x_axis_config={"numbers_to_include": [-6, -4, -2, 2, 4, 6]}, y_axis_config={"numbers_to_include": [-2, -1, 1, 2]}).shift(DOWN * 0.55)
        for l in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers: l.set_color(GRIS)
        seno = ejes.plot(np.sin, x_range=[-8, 8], color=AZUL, stroke_width=5)
        tit = MathTex(r"f(x)=\sin x", font_size=34, color=AZUL).to_corner(UL, buff=0.35)
        self.add(ejes); self.play(Create(seno), FadeIn(tit), run_time=1.2)
        formulas = {1: r"x", 3: r"x-\frac{x^3}{3!}", 5: r"x-\frac{x^3}{3!}+\frac{x^5}{5!}", 7: r"x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}"}
        cur = None; lab = None
        for n in [1, 3, 5, 7, 9, 11, 13, 15, 17]:
            p = P(n)
            def clip(x, p=p):
                return float(np.clip(p(x), -3.2, 3.2))
            g = ejes.plot(clip, x_range=[-8, 8, 0.02], color=NARANJA, stroke_width=4, use_smoothing=False)
            txt = (r"P_{%d}(x)=%s" % (n, formulas[n])) if n in formulas else (r"P_{%d}(x)=x-\frac{x^3}{3!}+\cdots+\frac{x^{%d}}{%d!}" % (n, n, n) if (n // 2) % 2 == 0 else r"P_{%d}(x)=x-\frac{x^3}{3!}+\cdots-\frac{x^{%d}}{%d!}" % (n, n, n))
            nl = MathTex(txt, font_size=32, color=NARANJA).to_corner(UR, buff=0.35)
            if cur is None:
                self.play(Create(g), FadeIn(nl), run_time=1.0)
            else:
                self.play(ReplacementTransform(cur, g), ReplacementTransform(lab, nl), run_time=1.0)
            cur, lab = g, nl
            self.wait(0.7)
        nota = MathTex(r"\text{cuanto mayor es } n,\ \text{más lejos de } 0 \text{ es buena la aproximación}", font_size=28).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(nota)); self.wait(2.5)
