from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
VERDE = "#1e8449"
ROJO = "#c0392b"
GRIS = "#555555"
BANDA = "#f9e79f"
BANDAV = "#abebc6"

A = 2.0
f = lambda x: 0.4 * x ** 2 - 0.2 * x + 1
L = f(A)


def delta_de(eps):
    for d in np.linspace(2, 0.001, 4000):
        xs = np.linspace(A - d, A + d, 400)
        if np.all(np.abs(f(xs) - L) < eps):
            return d
    return 0.001


class EpsilonDelta(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=6.2, y_length=6.0,
                    axis_config={"color": GRIS, "include_tip": False}).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        self.add(ejes)
        graf = ejes.plot(f, x_range=[0, 3.6], color=AZUL, stroke_width=4).set_z_index(3)
        hueco = Circle(radius=0.08, color=AZUL, stroke_width=3, fill_color=WHITE, fill_opacity=1).move_to(ejes.c2p(A, L)).set_z_index(4)
        la = MathTex("a", font_size=34).next_to(ejes.c2p(A, 0), DOWN, buff=0.15)
        lL = MathTex("L", font_size=34).next_to(ejes.c2p(0, L), LEFT, buff=0.15)
        g1 = DashedLine(ejes.c2p(A, 0), ejes.c2p(A, L), color=GRIS, stroke_width=1.5)
        g2 = DashedLine(ejes.c2p(0, L), ejes.c2p(A, L), color=GRIS, stroke_width=1.5)
        self.play(Create(graf), run_time=1.2)
        self.play(FadeIn(hueco), FadeIn(la), FadeIn(lL), Create(g1), Create(g2), run_time=0.8)

        X = 2.0
        t0 = MathTex(r"\lim_{x\to a} f(x) = L", font_size=40).move_to([X, 3.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(t0), run_time=0.5)
        regla = VGroup(Tex(r"Si $x$ está en la banda \textbf{verde},", font_size=28, color=VERDE),
                       Tex(r"$f(x)$ está en la banda \textbf{amarilla}.", font_size=28, color="#b7950b")).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([X, 2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(regla), run_time=0.5)

        bandaH = bandaV = info = None
        for eps in [1.2, 0.6, 0.3, 0.12]:
            d = delta_de(eps)
            nH = Rectangle(width=ejes.c2p(4, 0)[0] - ejes.c2p(0, 0)[0], height=ejes.c2p(0, L + eps)[1] - ejes.c2p(0, L - eps)[1],
                           fill_color=BANDA, fill_opacity=0.75, stroke_width=0).move_to(ejes.c2p(2, L)).set_z_index(-2)
            nV = Rectangle(width=ejes.c2p(A + d, 0)[0] - ejes.c2p(A - d, 0)[0], height=ejes.c2p(0, 5)[1] - ejes.c2p(0, 0)[1],
                           fill_color=BANDAV, fill_opacity=0.6, stroke_width=0).move_to(ejes.c2p(A, 2.5)).set_z_index(-1)
            tramo = ejes.plot(f, x_range=[A - d, A + d], color=ROJO, stroke_width=6).set_z_index(5)
            ni = VGroup(MathTex(r"\varepsilon = %.2f" % eps, font_size=34, color="#b7950b"),
                        MathTex(r"\delta \approx %.3f" % d, font_size=34, color=VERDE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([X, 0.6, 0], aligned_edge=LEFT)
            if bandaH is None:
                bandaH, bandaV, info, tr = nH, nV, ni, tramo
                self.play(FadeIn(bandaH), run_time=0.8)
                self.play(FadeIn(bandaV), FadeIn(info[0]), run_time=0.8)
                self.play(FadeIn(info[1]), Create(tr), run_time=0.8)
            else:
                self.play(Transform(bandaH, nH), Transform(info[0], ni[0]), FadeOut(tr), run_time=0.9)
                self.play(Transform(bandaV, nV), Transform(info[1], ni[1]), run_time=0.9)
                tr = tramo
                self.play(Create(tr), run_time=0.6)
            self.wait(0.8)
        cierre = VGroup(Tex(r"Para cada $\varepsilon>0$ hay un $\delta>0$:", font_size=28),
                        MathTex(r"0<|x-a|<\delta \ \Rightarrow\ |f(x)-L|<\varepsilon", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([X, -1.3, 0], aligned_edge=LEFT)
        nota = Tex(r"(El valor $f(a)$ no importa.)", font_size=26, color=GRIS).next_to(cierre, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(cierre), FadeIn(nota), run_time=0.8)
        self.wait(3)
