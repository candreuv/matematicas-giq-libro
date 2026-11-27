from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#2e8b57"
ROJO = "#c0392b"
GRIS = "#555555"
BANDA = "#f9e79f"

N_MAX = 30


def a(n):
    return -1 / n


def c(n):
    return 1 / n


def b(n):
    return math.sin(n) / n


class Sandwich(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        ejes = Axes(
            x_range=[0, N_MAX + 1, 5],
            y_range=[-1.1, 1.1, 0.5],
            x_length=10.5,
            y_length=4.9,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(5, N_MAX + 1, 5), "label_direction": DOWN},
            y_axis_config={"numbers_to_include": [-1, -0.5, 0.5, 1]},
        ).to_edge(DOWN, buff=0.45).shift(LEFT * 0.3)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        # números del eje x debajo del todo
        for lab in ejes.get_x_axis().numbers:
            lab.move_to([lab.get_x(), ejes.c2p(0, -1.1)[1] - 0.3, 0])
        etiq_n = MathTex("n", font_size=32).next_to(ejes.c2p(N_MAX + 1, 0), RIGHT, buff=0.15)

        titulo = MathTex(
            r"-\frac{1}{n}", r"\ \leq\ ", r"\frac{\sin n}{n}", r"\ \leq\ ", r"\frac{1}{n}",
            font_size=40,
        ).to_edge(UP, buff=0.3)
        titulo[0].set_color(AZUL)
        titulo[2].set_color(ROJO)
        titulo[4].set_color(VERDE)

        self.add(ejes, etiq_n)
        self.play(Write(titulo), run_time=1.2)

        # Región entre las dos sucesiones que hacen de "pan"
        pts_sup = [ejes.c2p(n, c(n)) for n in range(1, N_MAX + 1)]
        pts_inf = [ejes.c2p(n, a(n)) for n in range(N_MAX, 0, -1)]
        region = Polygon(*pts_sup, *pts_inf, fill_color=BANDA, fill_opacity=0.6, stroke_width=0)

        sup = VGroup(*[Dot(ejes.c2p(n, c(n)), radius=0.055, color=VERDE) for n in range(1, N_MAX + 1)])
        inf = VGroup(*[Dot(ejes.c2p(n, a(n)), radius=0.055, color=AZUL) for n in range(1, N_MAX + 1)])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in sup], lag_ratio=0.05),
                  LaggedStart(*[FadeIn(p, scale=0.5) for p in inf], lag_ratio=0.05), run_time=2)
        self.bring_to_back(region)
        self.play(FadeIn(region), run_time=0.8)

        txt_pan = Tex(r"Las dos sucesiones exteriores tienden a $0$\dots", font_size=30).next_to(titulo, DOWN, buff=0.2)
        self.play(FadeIn(txt_pan), run_time=0.6)
        self.wait(0.8)

        med = VGroup(*[Dot(ejes.c2p(n, b(n)), radius=0.065, color=ROJO) for n in range(1, N_MAX + 1)])
        txt_rel = Tex(r"\dots y la de en medio queda atrapada entre ellas", font_size=30).move_to(txt_pan)
        self.play(FadeOut(txt_pan), FadeIn(txt_rel), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in med], lag_ratio=0.12), run_time=3.2)
        self.wait(0.6)

        cero = DashedLine(ejes.c2p(0, 0), ejes.c2p(N_MAX + 1, 0), color=BLACK, stroke_width=2)
        concl = MathTex(
            r"\lim_{n\to\infty}\left(-\frac1n\right) = \lim_{n\to\infty}\frac1n = 0"
            r"\ \Longrightarrow\ \lim_{n\to\infty}\frac{\sin n}{n} = 0",
            font_size=32,
        ).move_to(txt_rel)
        self.play(Create(cero), FadeOut(txt_rel), FadeIn(concl), run_time=1)
        self.wait(3)
