from manim import *
import numpy as np
from scipy.integrate import quad
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"
f = lambda t: 1.2 + 0.9 * np.sin(1.4 * t)
G = lambda x: quad(f, 0, x)[0]

class TFC(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax1 = Axes(x_range=[0, 4.5, 1], y_range=[0, 2.5, 1], x_length=5.6, y_length=3.6,
                   axis_config={"color": GRIS, "include_tip": False, "font_size": 20}, x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
                   y_axis_config={"numbers_to_include": [1, 2]}).shift(LEFT * 3.4 + DOWN * 0.7)
        ax2 = Axes(x_range=[0, 4.5, 1], y_range=[0, 6, 2], x_length=5.6, y_length=3.6,
                   axis_config={"color": GRIS, "include_tip": False, "font_size": 20}, x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
                   y_axis_config={"numbers_to_include": [2, 4, 6]}).shift(RIGHT * 3.4 + DOWN * 0.7)
        for a in (ax1, ax2):
            for l in a.get_x_axis().numbers + a.get_y_axis().numbers: l.set_color(GRIS)
        gf = ax1.plot(f, x_range=[0, 4.3], color=AZUL, stroke_width=5)
        t1 = MathTex(r"y=f(t)", font_size=30, color=AZUL).next_to(ax1, UP, buff=0.15)
        t2 = MathTex(r"g(x)=\int_0^x f(t)\,dt", font_size=30, color=VERDE).next_to(ax2, UP, buff=0.05)
        self.add(ax1, ax2); self.play(Create(gf), FadeIn(t1), FadeIn(t2), run_time=1.2)
        xt = ValueTracker(0.01)
        area = always_redraw(lambda: ax1.get_area(gf, x_range=[0, xt.get_value()], color=VERDE, opacity=0.35))
        vline = always_redraw(lambda: DashedLine(ax1.c2p(xt.get_value(), 0), ax1.c2p(xt.get_value(), f(xt.get_value())), color=NARANJA, stroke_width=3))
        gg = always_redraw(lambda: ax2.plot(G, x_range=[0, max(xt.get_value(), 0.02), 0.05], color=VERDE, stroke_width=5))
        dot = always_redraw(lambda: Dot(ax2.c2p(xt.get_value(), G(xt.get_value())), color=BLACK, radius=0.06))
        def tang():
            x = xt.get_value(); y = G(x); m = f(x)
            sx = ax2.x_length / 4.5; sy = ax2.y_length / 6
            d = 0.6 / np.sqrt(sx ** 2 + (m * sy) ** 2) * 1.0
            return Line(ax2.c2p(x - d * 1.2, y - m * d * 1.2), ax2.c2p(x + d * 1.2, y + m * d * 1.2), color=NARANJA, stroke_width=4)
        tan = always_redraw(tang)
        info = always_redraw(lambda: MathTex(r"g'(x)=f(x)=%.2f" % f(xt.get_value()), font_size=32, color=NARANJA).to_edge(UP, buff=0.25))
        self.add(area, vline, gg, dot, tan, info)
        self.play(xt.animate.set_value(4.2), run_time=7, rate_func=linear)
        self.wait(0.5)
        nota = MathTex(r"\text{la pendiente de } g \text{ en } x \text{ es la altura de } f \text{ en } x", font_size=28).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(nota)); self.wait(2.5)
