from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
NARANJA = "#d35400"
ROJO = "#c0392b"
GRIS = "#555555"

N = 60
H = [0.0]
P2 = [0.0]
for n in range(1, N + 1):
    H.append(H[-1] + 1 / n)
    P2.append(P2[-1] + 1 / n ** 2)


class Armonica(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Sumas parciales: armónica frente a $p = 2$", font_size=36).to_edge(UP, buff=0.25)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, N + 1, 10], y_range=[0, 5, 1],
            x_length=7.0, y_length=5.2,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(10, N + 1, 10)},
            y_axis_config={"numbers_to_include": range(1, 6)},
        ).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        et_n = MathTex("n", font_size=30).next_to(ejes.c2p(N + 1, 0), RIGHT, buff=0.15)
        self.add(ejes, et_n)

        lim = DashedLine(ejes.c2p(0, math.pi ** 2 / 6), ejes.c2p(N + 1, math.pi ** 2 / 6), color=NARANJA, stroke_width=2)
        et_lim = MathTex(r"\tfrac{\pi^2}{6} \approx 1.645", font_size=26, color=NARANJA).next_to(ejes.c2p(48, math.pi ** 2 / 6), DOWN, buff=0.15)

        X_INFO = 2.3
        l1 = MathTex(r"H_n = 1 + \tfrac12 + \tfrac13 + \dots + \tfrac1n", font_size=30, color=AZUL).move_to([X_INFO, 2.45, 0], aligned_edge=LEFT)
        l2 = MathTex(r"P_n = 1 + \tfrac14 + \tfrac19 + \dots + \tfrac{1}{n^2}", font_size=30, color=NARANJA).move_to([X_INFO, 1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)

        t = ValueTracker(1)
        def puntos(S, color):
            def f():
                m = int(t.get_value())
                g = VGroup(*[Dot(ejes.c2p(n, S[n]), radius=0.04, color=color) for n in range(1, m + 1)])
                return g
            return f
        ph = always_redraw(puntos(H, AZUL))
        pp = always_redraw(puntos(P2, NARANJA))
        vh = always_redraw(lambda: MathTex(rf"H_{{{int(t.get_value())}}} \approx {H[int(t.get_value())]:.3f}", font_size=30, color=AZUL).move_to([X_INFO, 1.85, 0], aligned_edge=LEFT))
        vp = always_redraw(lambda: MathTex(rf"P_{{{int(t.get_value())}}} \approx {P2[int(t.get_value())]:.3f}", font_size=30, color=NARANJA).move_to([X_INFO, 0.6, 0], aligned_edge=LEFT))
        self.add(ph, pp, vh, vp)
        self.play(Create(lim), FadeIn(et_lim), run_time=0.6)
        self.play(t.animate.set_value(N), run_time=7, rate_func=linear)
        self.wait(0.5)

        n1 = Tex(r"$P_n$ se estabiliza: \textbf{converge}", font_size=26, color=NARANJA).move_to([X_INFO, -0.3, 0], aligned_edge=LEFT)
        n2 = Tex(r"$H_n$ crece sin límite, muy despacio:", font_size=26, color=AZUL).move_to([X_INFO, -0.9, 0], aligned_edge=LEFT)
        n3 = MathTex(r"H_{1000} \approx 7.49,\quad H_{10^6} \approx 14.39", font_size=26, color=AZUL).move_to([X_INFO, -1.4, 0], aligned_edge=LEFT)
        n4 = Tex(r"\textbf{diverge}, aunque $\tfrac1n \to 0$", font_size=26, color=AZUL).move_to([X_INFO, -1.95, 0], aligned_edge=LEFT)
        self.play(FadeIn(n1), run_time=0.6)
        self.play(FadeIn(n2), FadeIn(n3), run_time=0.8)
        self.play(FadeIn(n4), run_time=0.6)
        self.wait(3)
