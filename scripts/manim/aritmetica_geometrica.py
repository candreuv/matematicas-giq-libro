from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"

N_MAX = 16
D = 1.0      # diferencia de la aritmética
R = 1.25     # razón de la geométrica


def arit(n):
    return 1 + D * n


def geom(n):
    return R ** n


class AritmeticaGeometrica(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        ejes = Axes(
            x_range=[0, N_MAX + 0.5, 2],
            y_range=[0, 36, 5],
            x_length=10.5,
            y_length=5.0,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(2, N_MAX + 1, 2)},
            y_axis_config={"numbers_to_include": range(5, 36, 5)},
        ).to_edge(DOWN, buff=0.55).shift(LEFT * 0.4)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        etiq_n = MathTex("n", font_size=34).next_to(ejes.x_axis.get_end(), RIGHT, buff=0.2)

        tit_a = MathTex(r"a_n = a_{n-1} + 1", r"\ \ (\text{sumar})", color=AZUL, font_size=36)
        tit_g = MathTex(r"b_n = 1.25\, b_{n-1}", r"\ \ (\text{multiplicar})", color=NARANJA, font_size=36)
        titulos = VGroup(tit_a, tit_g).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.35)

        self.add(ejes, etiq_n)
        self.play(Write(titulos), run_time=1.2)

        pa = [Dot(ejes.c2p(n, arit(n)), radius=0.065, color=AZUL) for n in range(N_MAX + 1)]
        pg = [Dot(ejes.c2p(n, geom(n)), radius=0.065, color=NARANJA) for n in range(N_MAX + 1)]

        # Saltos: segmento vertical que muestra cuánto se añade en cada paso
        for n in range(N_MAX + 1):
            anims = [FadeIn(pa[n], scale=0.5), FadeIn(pg[n], scale=0.5)]
            if n > 0:
                anims += [
                    Create(Line(ejes.c2p(n, arit(n - 1)), ejes.c2p(n, arit(n)), color=AZUL, stroke_width=2)),
                    Create(Line(ejes.c2p(n, geom(n - 1)), ejes.c2p(n, geom(n)), color=NARANJA, stroke_width=2)),
                ]
            self.play(*anims, run_time=0.35 if n < 10 else 0.5)

        # Punto de cruce: la geométrica supera a la aritmética a partir de n = 12
        cruce = next(n for n in range(1, N_MAX + 1) if geom(n) > arit(n))
        circ = Circle(radius=0.22, color=BLACK, stroke_width=2.5).move_to(ejes.c2p(cruce, geom(cruce)))
        nota = Tex(
            rf"A partir de $n={cruce}$, la geométrica supera a la aritmética",
            font_size=30,
        ).next_to(titulos, DOWN, buff=0.3)
        self.play(Create(circ), FadeIn(nota), run_time=1)
        self.wait(1.2)

        sal_a = MathTex(r"\text{saltos iguales: } +1", color=AZUL, font_size=30)
        sal_g = MathTex(r"\text{saltos cada vez mayores: } \times 1.25", color=NARANJA, font_size=30)
        saltos = VGroup(sal_a, sal_g).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        saltos.move_to(ejes.c2p(4.5, 24))
        self.play(FadeIn(saltos), run_time=0.8)
        self.wait(3)
