from manim import *
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"
f = lambda t: 1.3 + 0.8 * np.sin(1.2 * t)
X0 = 2.0

def ch(h):
    m = quad(f, X0, X0 + h)[0] / h
    return brentq(lambda c: f(c) - m, X0, X0 + h)

class TFCDemo(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax = Axes(x_range=[0, 4.5, 1], y_range=[0, 2.5, 1], x_length=6.4, y_length=3.8,
                  axis_config={"color": GRIS, "include_tip": False, "font_size": 20},
                  x_axis_config={"numbers_to_include": [1, 3, 4]}, y_axis_config={"numbers_to_include": [1, 2]}).shift(LEFT * 3.1 + DOWN * 1.2)
        for l in ax.get_x_axis().numbers + ax.get_y_axis().numbers: l.set_color(GRIS)
        gf = ax.plot(f, x_range=[0, 4.4], color=AZUL, stroke_width=5)
        self.add(ax); self.play(Create(gf), run_time=1)
        area = ax.get_area(gf, x_range=[0, X0], color=VERDE, opacity=0.3)
        lx = MathTex("x", font_size=32).next_to(ax.c2p(X0, 0), DOWN, buff=0.12)
        t1 = MathTex(r"g(x)=\int_0^x f(t)\,dt", font_size=32, color=VERDE).move_to([3.0, 3.3, 0])
        self.play(FadeIn(area), FadeIn(lx), FadeIn(t1))
        ht = ValueTracker(1.6)
        strip = always_redraw(lambda: ax.get_area(gf, x_range=[X0, X0 + ht.get_value()], color=NARANJA, opacity=0.45))
        lxh = always_redraw(lambda: MathTex("x+h", font_size=28).set_opacity(1 if ht.get_value() > 0.4 else 0).next_to(ax.c2p(X0 + ht.get_value(), 0), DOWN, buff=0.12))
        t2 = MathTex(r"g(x+h)-g(x)=\int_x^{x+h}f(t)\,dt", font_size=30, color=NARANJA).next_to(t1, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(strip), FadeIn(lxh), FadeIn(t2))
        def rect():
            h = ht.get_value(); c = ch(h); y = f(c)
            return Polygon(ax.c2p(X0, 0), ax.c2p(X0 + h, 0), ax.c2p(X0 + h, y), ax.c2p(X0, y), stroke_color=BLACK, stroke_width=3, fill_opacity=0)
        def cdot():
            c = ch(ht.get_value()); return Dot(ax.c2p(c, f(c)), color=BLACK, radius=0.07)
        r = always_redraw(rect); d = always_redraw(cdot)
        t3 = MathTex(r"=f(c_h)\,h", font_size=30).next_to(t2, DOWN, aligned_edge=LEFT)
        t3b = Tex(r"(rectángulo de igual área,\\ teorema del valor medio)", font_size=24, color=GRIS).next_to(t3, RIGHT, buff=0.3)
        self.play(Create(r), FadeIn(d), FadeIn(t3), FadeIn(t3b))
        panel = always_redraw(lambda: VGroup(
            MathTex(r"h=%.2f" % ht.get_value(), font_size=34),
            MathTex(r"\frac{g(x+h)-g(x)}{h}=f(c_h)=%.3f" % f(ch(ht.get_value())), font_size=30, color=NARANJA),
            MathTex(r"f(x)=%.3f" % f(X0), font_size=30, color=AZUL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -1.6, 0]))
        self.add(panel); self.wait(0.8)
        self.play(ht.animate.set_value(0.05), run_time=6, rate_func=smooth)
        nota = MathTex(r"h\to0:\ c_h\to x\ \Rightarrow\ g'(x)=f(x)", font_size=34).move_to([3.6, -3.2, 0])
        self.play(FadeIn(nota)); self.wait(2.5)
