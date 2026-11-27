from manim import *
import math

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"


class Inversa(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-3, 5, 1], y_range=[-3, 5, 1], x_length=6.4, y_length=6.4,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 24},
                    x_axis_config={"numbers_to_include": [-2, 2, 4]},
                    y_axis_config={"numbers_to_include": [-2, 2, 4]}).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        self.add(ejes)
        diag = DashedLine(ejes.c2p(-3, -3), ejes.c2p(5, 5), color=GRIS, stroke_width=2)
        et_d = MathTex("y = x", font_size=28, color=GRIS).next_to(ejes.c2p(4.6, 4.6), RIGHT, buff=0.1).shift(DOWN * 0.3)
        expo = ejes.plot(lambda x: math.exp(x), x_range=[-3, math.log(5)], color=AZUL, stroke_width=4)
        et_e = MathTex("y = e^x", font_size=32, color=AZUL).move_to(ejes.c2p(0.3, 4.4)).shift(LEFT * 0.9)
        self.play(Create(diag), FadeIn(et_d), run_time=0.8)
        self.play(Create(expo), FadeIn(et_e), run_time=1.2)

        X = 3.0
        info = VGroup(Tex(r"Cada punto $(a,\ e^a)$", font_size=30, color=AZUL),
                      Tex(r"se refleja en $(e^a,\ a)$", font_size=30, color=NARANJA)).arrange(DOWN, aligned_edge=LEFT).move_to([X, 2.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(info), run_time=0.5)

        a = ValueTracker(-2.8)
        P = always_redraw(lambda: Dot(ejes.c2p(a.get_value(), math.exp(a.get_value())), color=AZUL, radius=0.08))
        Q = always_redraw(lambda: Dot(ejes.c2p(math.exp(a.get_value()), a.get_value()), color=NARANJA, radius=0.08))
        seg = always_redraw(lambda: DashedLine(P.get_center(), Q.get_center(), color=GRIS, stroke_width=1.5))
        traza = TracedPath(Q.get_center, stroke_color=NARANJA, stroke_width=4)
        val = always_redraw(lambda: VGroup(
            MathTex(r"a = %.2f" % a.get_value(), font_size=28),
            MathTex(r"(%.2f,\ %.2f) \ \to\ (%.2f,\ %.2f)" % (a.get_value(), math.exp(a.get_value()), math.exp(a.get_value()), a.get_value()), font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([X, 1.2, 0], aligned_edge=LEFT))
        self.add(traza, seg, P, Q, val)
        self.play(a.animate.set_value(math.log(4.9)), run_time=6, rate_func=linear)
        self.remove(val)
        et_l = MathTex(r"y = \ln x", font_size=32, color=NARANJA).move_to(ejes.c2p(4.2, 0.9))
        self.play(FadeIn(et_l), run_time=0.5)
        notas = VGroup(Tex(r"Las gráficas de $f$ y $f^{-1}$", font_size=28),
                       Tex(r"son simétricas respecto", font_size=28),
                       Tex(r"de la recta $y = x$.", font_size=28),
                       MathTex(r"e^{\ln x} = x,\qquad \ln(e^x) = x", font_size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([X, 0.4, 0], aligned_edge=LEFT)
        notas[3].shift(DOWN * 0.2)
        self.play(FadeIn(notas), run_time=0.8)
        self.wait(3)
