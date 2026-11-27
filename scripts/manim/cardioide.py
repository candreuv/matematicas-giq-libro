from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"
VERDE = "#1e8449"

g = lambda t: 1 + np.sin(t)


class Cardioide(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        plano = PolarPlane(radius_max=2.2, size=5.2, azimuth_step=12, radius_step=1,
                           background_line_style={"stroke_color": GRIS, "stroke_width": 0.8, "stroke_opacity": 0.4}).shift(LEFT * 3.4 + DOWN * 0.3)
        u = 5.2 / 2 / 2.2
        O = plano.get_center()
        self.add(plano)
        ejes = Axes(x_range=[0, 2 * PI + 0.1, PI / 2], y_range=[0, 2.2, 1], x_length=5.2, y_length=3.0,
                    axis_config={"color": GRIS, "include_tip": False}, y_axis_config={"numbers_to_include": [1, 2]}).shift(RIGHT * 3.4 + DOWN * 0.6)
        for lab in ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        etq = VGroup(*[MathTex(s, font_size=24, color=GRIS).next_to(ejes.c2p(k * PI / 2, 0), DOWN, buff=0.12) for k, s in [(1, r"\tfrac{\pi}{2}"), (2, r"\pi"), (3, r"\tfrac{3\pi}{2}"), (4, r"2\pi")]])
        et_th = MathTex(r"\theta", font_size=30).next_to(ejes.c2p(2 * PI + 0.1, 0), RIGHT, buff=0.1)
        et_r = MathTex(r"r", font_size=30).next_to(ejes.c2p(0, 2.2), UP, buff=0.1)
        self.add(ejes, etq, et_th, et_r)
        tit = MathTex(r"r = 1 + \sin\theta", font_size=42, color=AZUL).to_edge(UP, buff=0.3)
        self.play(FadeIn(tit), run_time=0.5)

        th = ValueTracker(0.0)

        def P():
            t = th.get_value()
            return O + u * g(t) * np.array([np.cos(t), np.sin(t), 0])
        rayo = always_redraw(lambda: Line(O, O + 2.3 * u * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0]), color=GRIS, stroke_width=1.5))
        seg = always_redraw(lambda: Line(O, P(), color=NARANJA, stroke_width=4))
        punto = always_redraw(lambda: Dot(P(), color=AZUL, radius=0.08))
        traza = TracedPath(punto.get_center, stroke_color=AZUL, stroke_width=4)
        pg = always_redraw(lambda: Dot(ejes.c2p(th.get_value(), g(th.get_value())), color=AZUL, radius=0.07))
        bar = always_redraw(lambda: Line(ejes.c2p(th.get_value(), 0), ejes.c2p(th.get_value(), g(th.get_value())), color=NARANJA, stroke_width=4))
        traza2 = TracedPath(pg.get_center, stroke_color=AZUL, stroke_width=3)
        val = always_redraw(lambda: MathTex(r"\theta = %.2f,\quad r = %.2f" % (th.get_value(), g(th.get_value())), font_size=30).move_to(RIGHT * 3.4 + UP * 2.0))
        self.add(traza, traza2, rayo, seg, punto, pg, bar, val)
        self.play(th.animate.set_value(PI / 2), run_time=2.2, rate_func=linear)
        self.wait(0.4)
        self.play(th.animate.set_value(3 * PI / 2), run_time=4.4, rate_func=linear)
        cus = Tex(r"$r=0$: cúspide en el origen", font_size=26, color=NARANJA).next_to(O, DOWN, buff=0.55)
        self.play(FadeIn(cus), run_time=0.4)
        self.wait(0.6)
        self.play(th.animate.set_value(2 * PI), run_time=2.2, rate_func=linear)
        nota = Tex(r"Paramétricas: $x=(1+\sin\theta)\cos\theta,\ \ y=(1+\sin\theta)\sin\theta$", font_size=28).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(nota), run_time=0.6)
        self.wait(3)
