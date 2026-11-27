from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"
f = lambda x: x ** 3 - 3 * x + 2
df = lambda x: 3 * x ** 2 - 3
a, b = -2.0, 2.0
m = (f(b) - f(a)) / (b - a)
cs = [-2 / np.sqrt(3), 2 / np.sqrt(3)]


class ValorMedio(Scene):
    def construct(self):
        Tex.set_default(color=BLACK); MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-2.4, 2.4, 1], y_range=[-0.6, 4.8, 1], x_length=7, y_length=5.6,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                    x_axis_config={"numbers_to_include": [-2, -1, 1, 2]}, y_axis_config={"numbers_to_include": [1, 2, 3, 4]}).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        for l in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers: l.set_color(GRIS)
        graf = ejes.plot(f, x_range=[-2.1, 2.1], color=AZUL, stroke_width=4)
        A = Dot(ejes.c2p(a, f(a)), color=BLACK); B = Dot(ejes.c2p(b, f(b)), color=BLACK)
        eA = MathTex("A", font_size=30).next_to(A, DL, buff=0.05); eB = MathTex("B", font_size=30).next_to(B, UR, buff=0.05)
        sec = Line(ejes.c2p(a, f(a)), ejes.c2p(b, f(b)), color=NARANJA, stroke_width=3)
        tit = MathTex(r"f(x) = x^3 - 3x + 2 \ \text{ en } [-2,\ 2]", font_size=32).to_corner(UR, buff=0.4)
        self.add(ejes); self.play(Create(graf), FadeIn(tit), run_time=1.2)
        self.play(FadeIn(A), FadeIn(B), FadeIn(eA), FadeIn(eB), Create(sec), run_time=0.8)
        X = 1.0
        ms = MathTex(r"\text{pendiente secante} = \frac{f(2)-f(-2)}{2-(-2)} = 1", font_size=28, color=NARANJA).move_to([X, 2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(ms), run_time=0.5)
        x = ValueTracker(-1.9)
        def tang():
            xx = x.get_value(); s = df(xx); L = 0.6
            return Line(ejes.c2p(xx - L, f(xx) - s * L), ejes.c2p(xx + L, f(xx) + s * L), color=VERDE, stroke_width=4)
        T = always_redraw(tang)
        P = always_redraw(lambda: Dot(ejes.c2p(x.get_value(), f(x.get_value())), color=VERDE, radius=0.08))
        val = always_redraw(lambda: MathTex(r"x = %.2f:\quad f'(x) = %.2f" % (x.get_value(), df(x.get_value())), font_size=30, color=VERDE).move_to([X, 1.2, 0], aligned_edge=LEFT))
        self.add(T, P, val)
        marcas = VGroup()
        for c in cs:
            self.play(x.animate.set_value(c), run_time=2.2, rate_func=smooth)
            mk = VGroup(Dot(ejes.c2p(c, f(c)), color=VERDE, radius=0.09), DashedLine(ejes.c2p(c, 0), ejes.c2p(c, f(c)), color=GRIS, stroke_width=1.5),
                        MathTex("c", font_size=32, color=VERDE).next_to(ejes.c2p(c, 0), DOWN, buff=0.5))
            fija = tang().set_stroke(opacity=0.5)
            self.play(FadeIn(mk), FadeIn(fija), Flash(ejes.c2p(c, f(c)), color=VERDE), run_time=0.8)
            marcas.add(mk, fija)
            self.wait(0.5)
        self.play(FadeOut(T), FadeOut(P), FadeOut(val), run_time=0.5)
        concl = VGroup(MathTex(r"f'(c) = 1 \ \Rightarrow\ c = \pm\tfrac{2}{\sqrt3} \approx \pm 1.15", font_size=30),
                       Tex(r"Tangente paralela a la secante", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([X, -0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)
