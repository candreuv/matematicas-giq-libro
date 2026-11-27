from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#2e8b57"
ROJO = "#c0392b"
GRIS = "#555555"
BANDA = "#f1c40f"

N_MAX = 30
L = 1.0


def a(n):
    return L + (-1) ** n / n


class BandaEpsilon(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        ejes = Axes(
            x_range=[0, N_MAX + 1, 5],
            y_range=[0, 2, 0.5],
            x_length=11,
            y_length=4.9,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(5, N_MAX + 1, 5)},
            y_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
        ).to_edge(DOWN, buff=0.6)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        etiq_n = MathTex("n", font_size=34).next_to(ejes.x_axis.get_end(), RIGHT, buff=0.2)
        etiq_a = MathTex("a_n", font_size=34).next_to(ejes.y_axis.get_end(), UP, buff=0.15)

        titulo = MathTex(
            r"a_n = 1 + \frac{(-1)^n}{n}\ \longrightarrow\ L = 1",
            font_size=40,
        ).to_edge(UP, buff=0.35)

        linea_L = DashedLine(
            ejes.c2p(0, L), ejes.c2p(N_MAX + 1, L), color=AZUL, stroke_width=3
        )
        etiq_L = MathTex("L", color=AZUL, font_size=34).next_to(linea_L, RIGHT, buff=0.1)

        puntos = VGroup(
            *[Dot(ejes.c2p(n, a(n)), radius=0.06, color=GRIS) for n in range(1, N_MAX + 1)]
        )

        self.add(ejes, etiq_n, etiq_a)
        self.play(Write(titulo), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in puntos], lag_ratio=0.08), run_time=2.5)
        self.play(Create(linea_L), FadeIn(etiq_L), run_time=0.8)
        self.wait(0.4)

        banda = None
        linea_M = None
        texto = None
        for eps in [0.5, 0.2, 0.1, 0.05]:
            M = int(round(1 / eps))  # |a_n - L| = 1/n < eps  <=>  n > 1/eps
            nueva_banda = Polygon(
                ejes.c2p(0, L - eps), ejes.c2p(N_MAX + 1, L - eps),
                ejes.c2p(N_MAX + 1, L + eps), ejes.c2p(0, L + eps),
                fill_color=BANDA, fill_opacity=0.35, stroke_width=0,
            )
            nueva_linea_M = DashedLine(
                ejes.c2p(M + 0.5, 0), ejes.c2p(M + 0.5, 2), color=ROJO, stroke_width=3
            )
            nuevo_texto = VGroup(
                MathTex(rf"\varepsilon = {eps}", font_size=36),
                MathTex(rf"M = {M}", font_size=36, color=ROJO),
            ).arrange(RIGHT, buff=0.6).next_to(titulo, DOWN, buff=0.25)
            colores = [
                p.animate.set_color(VERDE if n > M else GRIS)
                for n, p in zip(range(1, N_MAX + 1), puntos)
            ]
            if banda is None:
                self.play(FadeIn(nueva_banda), Write(nuevo_texto[0]), run_time=1)
                self.play(Create(nueva_linea_M), Write(nuevo_texto[1]), *colores, run_time=1.2)
            else:
                self.play(
                    Transform(banda, nueva_banda),
                    Transform(linea_M, nueva_linea_M),
                    Transform(texto, nuevo_texto),
                    *colores,
                    run_time=1.5,
                )
            if banda is None:
                banda, linea_M, texto = nueva_banda, nueva_linea_M, nuevo_texto
                self.bring_to_back(banda)
            self.wait(1.2)

        conclusion = Tex(
            r"Para cada $\varepsilon>0$ hay un $M$: a partir de él, todos los $a_n$ quedan en la banda",
            font_size=30,
        ).move_to(texto)
        self.play(FadeOut(texto), FadeIn(conclusion), run_time=0.8)
        self.wait(2.5)
