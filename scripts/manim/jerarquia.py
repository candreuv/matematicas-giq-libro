from manim import *
import math

config.background_color = WHITE

GRIS = "#555555"
COLORES = ["#7f8c8d", "#1f5fa8", "#2e8b57", "#d35400", "#8e44ad"]
NOMBRES = [r"\log n", r"n^2", r"2^n", r"n!", r"n^n"]
FUNCS = [
    lambda n: math.log(n) if n > 1 else 0.0,
    lambda n: n ** 2,
    lambda n: 2 ** n,
    lambda n: math.factorial(n),
    lambda n: n ** n,
]
N_MAX = 15
Y_MAX = 18  # escala log10


def lg(v):
    return math.log10(v) if v > 1 else 0.0


def fmt(v):
    if v < 1000:
        return f"{v:.1f}" if v != int(v) else f"{int(v)}"
    e = int(math.floor(math.log10(v)))
    m = v / 10 ** e
    return rf"{m:.1f}\cdot 10^{{{e}}}"


class Jerarquia(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Carrera de crecimientos (escala logarítmica)", font_size=36).to_edge(UP, buff=0.25)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, 5, 1], y_range=[0, Y_MAX, 3],
            x_length=7.5, y_length=5.3,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": True},
        ).to_edge(LEFT, buff=0.9).shift(DOWN * 0.35)
        marcas = VGroup(*[
            MathTex(rf"10^{{{k}}}", font_size=24, color=GRIS).next_to(ejes.c2p(0, k), LEFT, buff=0.12)
            for k in range(0, Y_MAX + 1, 3)
        ])
        self.add(ejes, marcas)

        ancho = 1.05
        xs = [0.5 + i for i in range(5)]
        etiquetas = VGroup(*[
            MathTex(NOMBRES[i], font_size=32, color=COLORES[i]).next_to(ejes.c2p(xs[i], 0), DOWN, buff=0.2)
            for i in range(5)
        ])
        self.add(etiquetas)

        def barras(n):
            g = VGroup()
            for i in range(5):
                h = max(lg(FUNCS[i](n)), 0.02)
                p0 = ejes.c2p(xs[i] - 0.38, 0)
                p1 = ejes.c2p(xs[i] + 0.38, h)
                r = Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01),
                              fill_color=COLORES[i], fill_opacity=0.85, stroke_width=0)
                r.move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
                g.add(r)
            return g

        def valores(n, bs):
            g = VGroup()
            for i in range(5):
                v = FUNCS[i](n)
                t = MathTex(fmt(v), font_size=20, color=COLORES[i]).next_to(bs[i], UP, buff=0.06)
                g.add(t)
            return g

        def ranking(n):
            orden = sorted(range(5), key=lambda i: FUNCS[i](n), reverse=True)
            g = VGroup(Tex(r"Clasificación", font_size=28))
            for pos, i in enumerate(orden):
                g.add(MathTex(rf"{pos+1}.\ {NOMBRES[i]}", font_size=30, color=COLORES[i]))
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            g.to_edge(RIGHT, buff=0.9).shift(DOWN * 0.2)
            return g

        n = 1
        bs = barras(n)
        vs = valores(n, bs)
        cont = MathTex(rf"n = {n}", font_size=40).to_corner(UR, buff=0.5).shift(DOWN * 0.6 + LEFT * 0.7)
        rk = ranking(n)
        self.play(FadeIn(bs), FadeIn(vs), FadeIn(cont), FadeIn(rk), run_time=1)

        for n in range(2, N_MAX + 1):
            nb = barras(n)
            nv = valores(n, nb)
            nc = MathTex(rf"n = {n}", font_size=40).move_to(cont)
            nr = ranking(n)
            self.play(Transform(bs, nb), Transform(vs, nv), Transform(cont, nc), Transform(rk, nr),
                      run_time=0.7 if n < 8 else 0.45)
            if n in (4, 5):
                self.wait(0.6)

        nota = MathTex(r"\log n \ll n^2 \ll 2^n \ll n! \ll n^n", font_size=30).next_to(rk, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        self.play(FadeIn(nota), run_time=0.8)
        self.wait(3)
