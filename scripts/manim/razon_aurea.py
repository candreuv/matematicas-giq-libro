from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"
DORADO = "#b8860b"

PHI = (1 + 5 ** 0.5) / 2
N_MAX = 12

# Fibonacci con F_0 = F_1 = 1
F = [1, 1]
while len(F) < N_MAX + 3:
    F.append(F[-1] + F[-2])
B = [F[n + 1] / F[n] for n in range(N_MAX + 1)]  # b_n = F_{n+1}/F_n


class RazonAurea(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        ejes = Axes(
            x_range=[0, N_MAX + 0.5, 1],
            y_range=[0.8, 2.2, 0.2],
            x_length=7.2,
            y_length=5.0,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(0, N_MAX + 1, 2)},
            y_axis_config={"numbers_to_include": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                           "decimal_number_config": {"num_decimal_places": 1}},
        ).to_corner(DL, buff=0.55)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        etiq_n = MathTex("n", font_size=32).next_to(ejes.x_axis.get_end(), RIGHT, buff=0.15)

        titulo = MathTex(
            r"b_n = \frac{F_{n+1}}{F_n} \ \longrightarrow\ \varphi = \frac{1+\sqrt5}{2} \approx 1.618",
            font_size=38,
        ).to_edge(UP, buff=0.3)

        linea_phi = DashedLine(ejes.c2p(0, PHI), ejes.c2p(N_MAX + 0.5, PHI), color=DORADO, stroke_width=3)
        etiq_phi = MathTex(r"\varphi", color=DORADO, font_size=34).next_to(linea_phi, RIGHT, buff=0.1)

        # Tabla a la derecha
        X = [3.75, 4.55, 5.65]
        Y0 = 1.75
        cab = VGroup(*[MathTex(s, font_size=30).move_to(RIGHT * x + UP * Y0) for s, x in zip(["n", "F_n", "b_n"], X)])
        filas = VGroup()

        self.add(ejes, etiq_n)
        self.play(Write(titulo), run_time=1.2)
        self.play(Create(linea_phi), FadeIn(etiq_phi), FadeIn(cab), run_time=0.8)

        puntos = []
        prev = None
        for n in range(N_MAX + 1):
            color = NARANJA if B[n] > PHI else AZUL
            p = Dot(ejes.c2p(n, B[n]), radius=0.07, color=color)
            anims = [FadeIn(p, scale=0.5)]
            if prev is not None:
                anims.append(Create(Line(prev.get_center(), p.get_center(), color=GRIS, stroke_width=1.5)))
            if n <= 9:
                y = Y0 - 0.42 * (n + 1)
                fila = VGroup(*[MathTex(s, font_size=28).move_to(RIGHT * x + UP * y)
                                for s, x in zip([f"{n}", f"{F[n]}", f"{B[n]:.4f}"], X)])
                fila[2].set_color(color)
                filas.add(fila)
                anims.append(FadeIn(fila))
            self.play(*anims, run_time=0.55 if n < 6 else 0.4)
            puntos.append(p)
            prev = p

        nota = Tex(
            r"Oscilan por encima (naranja) y por debajo (azul) de $\varphi$, cada vez más cerca",
            font_size=26,
        ).next_to(titulo, DOWN, buff=0.2)
        self.play(FadeIn(nota), run_time=0.8)
        self.wait(3)
