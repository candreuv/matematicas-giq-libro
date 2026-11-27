from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#27ae60"
ROJO = "#c0392b"
GRIS = "#555555"
GRIS_CLARO = "#999999"
BANDA = "#f9e79f"

N_MAX = 20
L = 3.0
EPS = 0.3


def a(n):
    return 3 * n / (n + 1)


class Monotona(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = MathTex(r"a_n = \frac{3n}{n+1}:\quad \tfrac{3}{2},\ 2,\ \tfrac{9}{4},\ \tfrac{12}{5},\ \dots", font_size=36).to_edge(UP, buff=0.2)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, N_MAX + 0.5, 5], y_range=[1.25, 4.0, 0.25],
            x_length=7.2, y_length=5.3,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(5, N_MAX + 1, 5)},
            y_axis_config={"numbers_to_include": [1.5, 2, 2.5, 3, 3.5],
                           "decimal_number_config": {"num_decimal_places": 1}},
        ).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        etiq_n = MathTex("n", font_size=30).next_to(ejes.c2p(N_MAX + 0.5, 1.25), RIGHT, buff=0.15)
        self.add(ejes, etiq_n)

        X_TXT = 1.9

        def paso(texto, y):
            lineas = texto.split(r"\\")
            t = VGroup(*[Tex(l.strip(), font_size=25) for l in lineas]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            t.move_to([X_TXT, y, 0], aligned_edge=LEFT)
            return t

        t1 = paso(r"1. Es creciente: cada término\\ supera al anterior", 2.45)
        self.play(FadeIn(t1), run_time=0.5)

        puntos = VGroup()
        prev = None
        for n in range(1, N_MAX + 1):
            p = Dot(ejes.c2p(n, a(n)), radius=0.065, color=AZUL)
            anims = [FadeIn(p, scale=0.5)]
            if prev is not None:
                anims.append(Create(Line(prev.get_center(), p.get_center(), color=AZUL, stroke_width=1.5)))
            self.play(*anims, run_time=0.32)
            puntos.add(p)
            prev = p
        self.wait(0.4)

        t2 = paso(r"2. Está acotada superiormente:\\ 3.75, 3.5, 3.25\dots\ son cotas", 1.35)
        cotas = VGroup(*[DashedLine(ejes.c2p(0, y), ejes.c2p(N_MAX + 0.5, y), color=GRIS_CLARO, stroke_width=2)
                         for y in [3.75, 3.5, 3.25]])
        self.play(FadeIn(t2), LaggedStart(*[Create(l) for l in cotas], lag_ratio=0.3), run_time=1.5)
        self.wait(0.5)

        sup = Line(ejes.c2p(0, L), ejes.c2p(N_MAX + 0.5, L), color=ROJO, stroke_width=3.5)
        et_sup = MathTex(r"L = 3", color=ROJO, font_size=28).next_to(ejes.c2p(1.0, L), UP, buff=0.06)
        t3 = paso(r"3. La menor cota es el \textbf{supremo}\\ $L = 3$ (no se alcanza: no es máximo)", 0.25)
        self.play(FadeIn(t3), Create(sup), FadeIn(et_sup), run_time=1.2)
        self.wait(0.5)

        banda = Polygon(ejes.c2p(0, L - EPS), ejes.c2p(N_MAX + 0.5, L - EPS),
                        ejes.c2p(N_MAX + 0.5, L), ejes.c2p(0, L),
                        fill_color=BANDA, fill_opacity=0.85, stroke_width=0)
        self.bring_to_back(banda)
        M = next(n for n in range(1, N_MAX + 1) if a(n) > L - EPS)
        t4 = paso(rf"4. Para $\varepsilon = {EPS}$, desde $a_{{{M}}}$ todos\\ los términos están en $(L - \varepsilon,\ L]$", -0.85)
        self.play(FadeIn(banda), FadeIn(t4), run_time=1)
        self.play(*[puntos[n - 1].animate.set_color(VERDE) for n in range(M, N_MAX + 1)], run_time=0.8)
        self.wait(0.5)

        concl = MathTex(r"\text{Monótona + acotada} \ \Rightarrow\ \lim_{n\to\infty} a_n = 3", font_size=30, color=ROJO)
        concl.move_to([X_TXT, -2.1, 0], aligned_edge=LEFT)
        concl.scale(0.9).align_to(t4, LEFT)
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)
