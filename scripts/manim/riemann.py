from manim import *
import numpy as np
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; GRIS = "#555555"
f = lambda x: 0.2 * x ** 2 - 0.9 * x + 2.4 + 0.5 * np.sin(1.3 * x)
A, B = 0.5, 5.5
from scipy.integrate import quad
EXACT = quad(f, A, B)[0]

class Riemann(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4.5, 1], x_length=9.5, y_length=5,
                  axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                  x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]}, y_axis_config={"numbers_to_include": [1, 2, 3, 4]}).shift(DOWN * 0.35 + LEFT * 1.6)
        for l in ax.get_x_axis().numbers + ax.get_y_axis().numbers: l.set_color(GRIS)
        g = ax.plot(f, x_range=[0, 5.8], color=AZUL, stroke_width=5)
        la = MathTex("a", font_size=30).next_to(ax.c2p(A, 0), DOWN, buff=0.12)
        lb = MathTex("b", font_size=30).next_to(ax.c2p(B, 0), DOWN, buff=0.12)
        area = ax.get_area(g, x_range=[A, B], color=AZUL, opacity=0.25)
        tit = MathTex(r"\int_a^b f(x)\,dx", r"=\lim_{n\to\infty}\sum_{k=1}^{n} f(x_k^*)\,\Delta x", font_size=32).to_corner(UL, buff=0.3)
        self.add(ax); self.play(Create(g), FadeIn(la), FadeIn(lb), run_time=1)
        self.play(FadeIn(area), FadeIn(tit[0])); self.wait(0.5); self.play(FadeOut(area), FadeIn(tit[1]))
        panel_x = 4.9
        cur = None; txt = None
        for n in [2, 4, 8, 16, 32, 64]:
            dx = (B - A) / n
            rects = VGroup()
            s = 0
            for k in range(n):
                xm = A + (k + 0.5) * dx
                h = f(xm); s += h * dx
                r = Polygon(ax.c2p(A + k * dx, 0), ax.c2p(A + (k + 1) * dx, 0), ax.c2p(A + (k + 1) * dx, h), ax.c2p(A + k * dx, h),
                            fill_color=NARANJA, fill_opacity=0.45, stroke_color=NARANJA, stroke_width=1.5 if n < 32 else 0.6)
                rects.add(r)
            t = VGroup(MathTex(r"n=%d" % n, font_size=34),
                       MathTex(r"\Delta x=\tfrac{b-a}{n}", font_size=30),
                       MathTex(r"S_n=%.4f" % s, font_size=34, color=NARANJA),
                       MathTex(r"\text{área}=%.4f" % EXACT, font_size=30, color=AZUL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([panel_x, 0.3, 0])
            if cur is None:
                self.play(Create(rects), FadeIn(t), run_time=1.2)
            else:
                self.play(ReplacementTransform(cur, rects), ReplacementTransform(txt, t), run_time=1.0)
            cur, txt = rects, t
            self.bring_to_front(g)
            self.wait(0.8)
        nota = MathTex(r"\text{puntos muestra: puntos medios. Al refinar, } S_n \to \text{área}", font_size=28).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(nota)); self.wait(2.5)
