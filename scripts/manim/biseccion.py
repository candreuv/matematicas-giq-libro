from manim import *

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
VERDE = "#1e8449"
ROJO = "#c0392b"
GRIS = "#555555"
BANDAV = "#abebc6"

f = lambda x: x ** 3 - 3 * x + 1


class Biseccion(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-0.05, 1.05, 0.25], y_range=[-1.3, 1.3, 0.5], x_length=6.6, y_length=5.4,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                    x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1]},
                    y_axis_config={"numbers_to_include": [-1, 1]}).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        graf = ejes.plot(f, x_range=[0, 1], color=AZUL, stroke_width=4).set_z_index(2)
        tit = MathTex(r"f(x) = x^3 - 3x + 1", font_size=34, color=AZUL).to_edge(UP, buff=0.3).shift(LEFT * 3.3)
        self.add(ejes)
        self.play(Create(graf), FadeIn(tit), run_time=1.2)

        def signo(v):
            return "+" if v > 0 else "-"

        X = 1.6
        cab = MathTex(r"n \quad [a_n,\ b_n] \qquad\quad \text{error} \le", font_size=28).move_to([X, 3.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(cab), run_time=0.4)
        a, b = 0.0, 1.0
        filas = VGroup()
        banda = None
        for n in range(0, 7):
            nb = Rectangle(width=ejes.c2p(b, 0)[0] - ejes.c2p(a, 0)[0], height=ejes.c2p(0, 1.3)[1] - ejes.c2p(0, -1.3)[1],
                           fill_color=BANDAV, fill_opacity=0.55, stroke_width=0).move_to(ejes.c2p((a + b) / 2, 0)).set_z_index(-1)

            pa = Dot(ejes.c2p(a, f(a)), color=VERDE if f(a) > 0 else ROJO, radius=0.07).set_z_index(3)
            pb = Dot(ejes.c2p(b, f(b)), color=VERDE if f(b) > 0 else ROJO, radius=0.07).set_z_index(3)
            fila = MathTex(r"%d \quad [%.4f,\ %.4f] \quad %.4f" % (n, a, b, (b - a) / 2), font_size=28).move_to([X, 2.55 - 0.48 * n, 0], aligned_edge=LEFT)
            if banda is None:
                banda = nb
                self.play(FadeIn(banda), FadeIn(pa), FadeIn(pb), FadeIn(fila), run_time=0.8)
            else:
                self.play(Transform(banda, nb), FadeIn(pa), FadeIn(pb), FadeIn(fila), run_time=0.8)
            filas.add(fila)
            if n == 6:
                break
            m = (a + b) / 2
            lm = DashedLine(ejes.c2p(m, 0), ejes.c2p(m, f(m)), color=NARANJA, stroke_width=2)
            pm = Dot(ejes.c2p(m, f(m)), color=NARANJA, radius=0.08).set_z_index(4)
            sm = MathTex(r"f(m)%s0" % (">" if f(m) > 0 else "<"), font_size=26, color=NARANJA).next_to(pm, UR if f(m) > 0 else DR, buff=0.05)
            self.play(Create(lm), FadeIn(pm), FadeIn(sm), run_time=0.6 if n < 3 else 0.4)
            if f(a) * f(m) < 0:
                b = m
            else:
                a = m
            self.play(FadeOut(lm), FadeOut(pm), FadeOut(sm), FadeOut(pa), FadeOut(pb), run_time=0.3)
        raiz = MathTex(r"c \approx 0.3473", font_size=32, color=NARANJA).move_to([X, -1.3, 0], aligned_edge=LEFT)
        nota = Tex(r"Cada paso divide el error entre 2.", font_size=28).next_to(raiz, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(raiz), FadeIn(nota), run_time=0.8)
        self.wait(3)
