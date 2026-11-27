from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"


class Cicloide(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[0, 4 * PI + 0.3, PI], y_range=[0, 2.4, 1], x_length=12.5, y_length=2.4 * 12.5 / (4 * PI + 0.3),
                    axis_config={"color": GRIS, "include_tip": False}).to_edge(DOWN, buff=1.0).shift(LEFT * 0.25)
        etq = VGroup(*[MathTex(s, font_size=26, color=GRIS).next_to(ejes.c2p(k * PI, 0), DOWN, buff=0.15) for k, s in [(1, r"\pi"), (2, r"2\pi"), (3, r"3\pi"), (4, r"4\pi")]])
        etq_y = VGroup(*[MathTex(s, font_size=26, color=GRIS).next_to(ejes.c2p(0, k), LEFT, buff=0.15) for k, s in [(1, "1"), (2, "2")]])
        lx = MathTex("x", font_size=32).next_to(ejes.c2p(4 * PI + 0.3, 0), DR, buff=0.12)
        ly = MathTex("y", font_size=32).next_to(ejes.c2p(0, 2.4), UP, buff=0.12)
        self.add(ejes, etq, etq_y, lx, ly)
        tit = MathTex(r"\vec r(t) = (t - \sin t,\ 1 - \cos t)", font_size=40).to_edge(UP, buff=0.4)
        sub = Tex(r"Un punto del borde de una rueda de radio 1 que rueda sin deslizar", font_size=28, color=GRIS).next_to(tit, DOWN, buff=0.15)
        self.play(FadeIn(tit), FadeIn(sub), run_time=0.8)
        t = ValueTracker(0)
        u = ejes.x_axis.get_unit_size()

        def rueda():
            tt = t.get_value()
            c = Circle(radius=u, color=AZUL, stroke_width=3).move_to(ejes.c2p(tt, 1))
            radio = Line(ejes.c2p(tt, 1), ejes.c2p(tt - np.sin(tt), 1 - np.cos(tt)), color=AZUL, stroke_width=2)
            return VGroup(c, radio, Dot(ejes.c2p(tt, 1), radius=0.04, color=AZUL))
        r = always_redraw(rueda)
        P = always_redraw(lambda: Dot(ejes.c2p(t.get_value() - np.sin(t.get_value()), 1 - np.cos(t.get_value())), color=NARANJA, radius=0.08))
        traza = TracedPath(P.get_center, stroke_color=NARANJA, stroke_width=4)
        val = always_redraw(lambda: MathTex(r"t = %.2f" % t.get_value(), font_size=30).to_corner(UR, buff=0.4).shift(DOWN * 1.2))
        self.add(traza, r, P, val)
        self.play(t.animate.set_value(4 * PI), run_time=9, rate_func=linear)
        nota = Tex(r"La cicloide: arcos de anchura $2\pi$ y altura $2$, con picos (cúspides) en el suelo", font_size=28).next_to(sub, DOWN, buff=0.3)
        self.play(FadeIn(nota), run_time=0.6)
        self.wait(2.5)
