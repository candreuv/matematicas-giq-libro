from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
NARANJA = "#d35400"
ROJO = "#c0392b"
GRIS = "#555555"
VERDE = "#27ae60"

NS = [1, 2, 4, 12, 52, 365]
NOMBRES = {1: "anual", 2: "semestral", 4: "trimestral", 12: "mensual", 52: "semanal", 365: "diaria"}


class NumeroE(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Interés compuesto del 100\,\% anual: 1 € durante un año", font_size=34).to_edge(UP, buff=0.25)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, 1.0, 0.25], y_range=[1, 2.9, 0.25],
            x_length=7.4, y_length=5.2,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                           "decimal_number_config": {"num_decimal_places": 2}},
            y_axis_config={"numbers_to_include": [1.0, 1.5, 2.0, 2.5],
                           "decimal_number_config": {"num_decimal_places": 1}},
        ).to_edge(DOWN, buff=0.75).to_edge(LEFT, buff=0.8)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        et_t = Tex(r"tiempo (años)", font_size=24, color=GRIS).next_to(ejes.c2p(0.5, 1), DOWN, buff=0.5)
        et_c = Tex(r"capital (€)", font_size=24, color=GRIS).next_to(ejes.y_axis.get_end(), UP, buff=0.1)
        self.add(ejes, et_t, et_c)

        linea_e = DashedLine(ejes.c2p(0, math.e), ejes.c2p(1.0, math.e), color=ROJO, stroke_width=2.5)
        et_e = MathTex(r"e \approx 2.71828", color=ROJO, font_size=28).next_to(ejes.c2p(0.02, math.e), UP, buff=0.08).align_to(ejes.c2p(0.02, 0), LEFT)

        def escalera(n):
            pts = []
            c = 1.0
            for k in range(n):
                t0, t1 = k / n, (k + 1) / n
                pts += [ejes.c2p(t0, c), ejes.c2p(t1, c)]
                c *= 1 + 1 / n
                pts.append(ejes.c2p(t1, c))
            return VMobject(color=AZUL, stroke_width=3).set_points_as_corners(pts)

        X_TAB = 2.1
        cab = VGroup(Tex(r"capitalización", font_size=26), MathTex(r"n", font_size=28),
                     MathTex(r"\left(1+\tfrac1n\right)^n", font_size=28))
        xs = [X_TAB, X_TAB + 2.55, X_TAB + 3.75]
        for m, x in zip(cab, xs):
            m.move_to([x, 2.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(cab), run_time=0.6)

        curva = None
        for j, n in enumerate(NS):
            nueva = escalera(n)
            v = (1 + 1 / n) ** n
            y = 1.8 - 0.52 * j
            fila = VGroup(Tex(NOMBRES[n], font_size=26), MathTex(rf"{n}", font_size=28),
                          MathTex(rf"{v:.5f}", font_size=28, color=AZUL))
            for m, x in zip(fila, xs):
                m.move_to([x, y, 0], aligned_edge=LEFT)
            punto = Dot(ejes.c2p(1.0, v), radius=0.07, color=AZUL)
            if curva is None:
                curva, p_fin = nueva, punto
                self.play(Create(curva), FadeIn(fila), FadeIn(p_fin), run_time=1.4)
            else:
                self.play(Transform(curva, nueva), p_fin.animate.move_to(ejes.c2p(1.0, v)), FadeIn(fila), run_time=1.2)
            self.wait(0.5)

        exp = ejes.plot(lambda t: math.exp(t), x_range=[0, 1], color=VERDE, stroke_width=3)
        et_exp = MathTex(r"C(t) = e^{t}", color=VERDE, font_size=28).next_to(ejes.c2p(0.55, math.exp(0.55)), UP + LEFT, buff=0.1)
        self.play(Create(linea_e), FadeIn(et_e), run_time=0.8)
        self.play(Create(exp), FadeIn(et_exp), run_time=1.2)
        concl = MathTex(r"\lim_{n\to\infty}\left(1+\frac1n\right)^n = e", font_size=36, color=ROJO)
        concl.move_to([X_TAB + 2.3, -1.75, 0])
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)
